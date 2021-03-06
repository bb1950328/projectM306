# coding=utf-8
import datetime
import decimal
import json
import urllib
from typing import Optional, List, Dict, Tuple, Union

from django.contrib.auth.models import User

import time_entry.model.entity.absence as absence
import time_entry.model.entity.employee as employee
import time_entry.model.entity.entry as entry
from time_entry.model import db, util
from time_entry.model.entity.project import Project
from time_entry.model.entity.setting import Setting


def new_employee(empl_nr, first_name, last_name):
    em = employee.Employee()
    em.emplNr = empl_nr
    em.firstName = first_name
    em.lastName = last_name
    em.insert()


def edit_employee(empl_nr, new_first_name=None, new_last_name=None):
    em = employee.Employee.find(empl_nr)
    if new_first_name is not None:
        em.firstName = new_first_name
    if new_last_name is not None:
        em.lastName = new_last_name
    em.save()


def new_project(project_nr, name, description):
    pr = Project()
    pr.nr = project_nr
    pr.name = name
    pr.description = description
    pr.insert()


def edit_project(project_nr, new_name=None, new_description=None):
    pr = Project.find(project_nr)
    if new_name is not None:
        pr.name = new_name
    if new_description is not None:
        pr.description = new_description
    pr.save()


def new_entry(project_nr, empl_nr, start, end):
    en = entry.Entry(project_nr, empl_nr)
    en._project_nr = project_nr
    en.start = start
    en.end = end
    en.insert()


def edit_entry(entry_id, new_project_nr=None, new_empl_nr=None, new_start=None, new_end=None):
    en = entry.Entry.find(entry_id)
    if new_project_nr is not None:
        en._project_nr = new_project_nr
    if new_empl_nr is not None:
        en._empl_nr = new_empl_nr
    if new_start is not None:
        en.start = new_start
    if new_end is not None:
        en.end = new_end
    en.save()


def add_user(username, password):
    User.objects.create_user(username, password=password)


def reset_password(username, new_password):
    user = User.objects.get(username)
    user.set_password(new_password)


def collect_entries(empl_nr: int, start: datetime.datetime, end: datetime.datetime):
    cur = db.get_conn().cursor()
    sql_start = util.datetime_to_sql(start)
    sql_end = util.datetime_to_sql(end)
    command = f"SELECT * FROM {entry.Entry.Table.name} " \
              f"WHERE emplNr={empl_nr} AND start_ > {sql_start} AND end_ < {sql_end}"
    print(command)
    cur.execute(command)
    return [entry.Entry.from_result(cur.column_names, res) for res in cur.fetchall()]


def get_all_projects_as_json() -> str:
    cur = db.get_conn().cursor()
    cur.execute(f"SELECT nr, name_ FROM {Project.Table.name}")
    result = {int(row[0]): row[1] for row in cur.fetchall()}
    cur.close()
    return json.dumps(result)


def calculate_worked_hours(empl_nr: int) -> float:
    cur = db.get_conn().cursor()
    command = f"SELECT SUM(TIMEDIFF(end_, start_)) FROM {entry.Entry.Table.name} " \
              f"WHERE emplNr={empl_nr} " \
              f"AND end_ <= {util.date_to_sql(datetime.date.today() + datetime.timedelta(days=1))}"
    print(command)
    cur.execute(command)
    res = cur.fetchone()[0]
    if res is None:
        res = decimal.Decimal("0")
    return res / 10_000  # TIMEDIFF() returns 10'000 per hour


def count_work_days(start: datetime.date, end: datetime.date) -> int:
    count = 0
    oneday = datetime.timedelta(days=1)
    while start <= end:
        if util.is_work_day(start):
            count += 1
        start += oneday
    return count


def calculate_float_time(empl_nr: int) -> decimal.Decimal:
    empl = employee.Employee.find(empl_nr)
    worked_hours = calculate_worked_hours(empl_nr)
    today = datetime.date.today()
    if empl.until:
        end = min(today, empl.until)
    else:
        end = today
    present_days = count_work_days(empl.since, end)
    present_days -= count_absent_days(empl_nr)
    soll_work: str = Setting.find(Setting.SOLL_WORK_PER_DAY).value
    should_worked = present_days * decimal.Decimal(soll_work)
    return worked_hours - should_worked


def save_changes(empl_nr, GET) -> Optional[List[str]]:
    changes = GET.get("save")
    if changes is None:
        return
    messages = []
    changes = urllib.parse.unquote(changes)
    loaded = json.loads(changes)
    time_format = "%Y-%m-%dT%H:%M"
    for entry_id, project_nr, start, end in loaded:
        start = datetime.datetime.strptime(start, time_format)
        end = datetime.datetime.strptime(end, time_format)
        try:
            if entry_id.startswith("new"):
                new_entry(project_nr, empl_nr, start, end)
            else:
                edit_entry(entry_id, project_nr, empl_nr, start, end)
        except ValueError as e:
            messages.append(", ".join(e.args))

    return messages if messages else None


def collect_absences(empl_nr, sort=False):
    cur = db.get_conn().cursor()
    command = f"SELECT * FROM {absence.Absence.Table.name} WHERE emplNr={empl_nr}"
    print(command)
    cur.execute(command)
    res = [absence.Absence.from_result(cur.column_names, res) for res in cur.fetchall()]
    if sort:
        res.sort(key=lambda ab: ab.start)
    return res


def count_absent_days(empl_nr: int) -> int:
    absences = collect_absences(empl_nr)
    today = datetime.date.today()
    count = 0
    for ab in absences:
        if ab.end <= today:
            count += ab.length
        elif ab.start <= today:  # we are inside of the absence now
            count += (today - ab.start + datetime.timedelta(days=1)).days
    return count


def add_absence(POST):
    ab = absence.Absence()
    ab._empl_nr = int(POST.get("emplNr"))
    ab.reason = POST.get("reason")
    ab.start = datetime.date.fromisoformat(POST.get("start"))
    ab.end = datetime.date.fromisoformat(POST.get("end"))
    ab.insert()


def collect_employees():
    cur = db.get_conn().cursor()
    cur.execute(f"SELECT * FROM {employee.Employee.Table.name}")
    result = [employee.Employee.from_result(cur.column_names, row) for row in cur.fetchall()]
    cur.close()
    return result


def collect_projects():
    cur = db.get_conn().cursor()
    cur.execute(f"SELECT * FROM {Project.Table.name}")
    result = [Project.from_result(cur.column_names, row) for row in cur.fetchall()]
    cur.close()
    return result


def get_contributors_for_project(project_nr):
    cur = db.get_conn().cursor()
    command = f"SELECT DISTINCT emplNr FROM {entry.Entry.Table.name} " \
              f"WHERE projectNr={project_nr}"
    cur.execute(command)
    result = cur.fetchall()
    cur.close()
    return [employee.Employee.find(int(row[0])) for row in result]


def calculate_hours_for_project(project_nr):
    cur = db.get_conn().cursor()
    command = f"SELECT SUM(TIMEDIFF(end_, start_)) FROM {entry.Entry.Table.name} " \
              f"WHERE projectNr={project_nr}"
    cur.execute(command)
    res = cur.fetchone()[0]
    cur.close()
    if res is None:
        res = decimal.Decimal("0")
    return res / 10_000  # TIMEDIFF() returns 10'000 per hour


def get_hours_per_day(project_nr: int):
    query = f"SELECT DATE(e.start_) AS 'date', SUM(TIMEDIFF(e.end_, e.start_))/10000 AS 'hours' " \
            f"FROM {entry.Entry.Table.name} AS e " \
            f"WHERE e.projectNr = {project_nr} " \
            f"GROUP BY DATE(e.start_);"
    cur = db.get_conn().cursor()
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    return res


def get_hours_per_day_for_all_projects() -> Dict[Project, List[Tuple[Union[datetime.date, decimal.Decimal]]]]:
    projects = collect_projects()
    return {pro: get_hours_per_day(pro.nr) for pro in projects}


def get_hours_per_employee_for_project(project_nr: int):
    query = f"SELECT projectNr, SUM(TIMEDIFF(end_, start_)/10000) AS 'hours' " \
            f"FROM {entry.Entry.Table.name} " \
            f"WHERE projectNr={project_nr} " \
            f"GROUP BY emplNr ORDER BY 'hours' DESC;"
    cur = db.get_conn().cursor()
    cur.execute(query)
    idx_emplnr = cur.column_names.index("emplNr")
    idx_hours = cur.column_names.index("hours")
    res = {employee.Employee.find(row[idx_emplnr]): row[idx_hours] for row in cur.fetchall()}
    cur.close()
    return res


def get_hours_per_project_for_employee(empl_nr: int):
    query = f"SELECT projectNr, SUM(TIMEDIFF(end_, start_)/10000) AS 'hours' " \
            f"FROM {entry.Entry.Table.name} " \
            f"WHERE emplNr={empl_nr} " \
            f"GROUP BY projectNr ORDER BY 'hours' DESC;"
    cur = db.get_conn().cursor()
    cur.execute(query)
    idx_emplnr = cur.column_names.index("projectNr")
    idx_hours = cur.column_names.index("hours")
    res = {Project.find(row[idx_emplnr]): row[idx_hours] for row in cur.fetchall()}
    cur.close()
    return res


def get_number_of_employees():
    query = f"SELECT since, until " \
            f"FROM {employee.Employee.Table.name} " \
            f"ORDER BY since ASC;"
    print(query)
    cur = db.get_conn().cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    start = data[0][0]
    end = datetime.date.today()
    days = [start + datetime.timedelta(days=x) for x in range((end - start).days + 1)]
    counts = []
    for day in days:
        num = 0
        for since, until in data:
            if (until is None and since < day) \
                    or (since < day < until):
                num += 1
        counts.append(num)
    return days, counts
