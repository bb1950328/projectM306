# coding=utf-8
import datetime
import decimal
import json
import urllib
from typing import Optional, List

from django.contrib.auth.models import User

import time_entry.model.entity.absence as absence
import time_entry.model.entity.employee as employee
import time_entry.model.entity.entry as entry
from time_entry.model import db, util, settings
from time_entry.model.entity.project import Project


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
    cur = db.conn.cursor()
    sql_start = util.datetime_to_sql(start)
    sql_end = util.datetime_to_sql(end)
    command = f"SELECT * FROM {entry.Entry.Table.name} " \
              f"WHERE emplNr={empl_nr} AND start_ > {sql_start} AND end_ < {sql_end}"
    print(command)
    cur.execute(command)
    return [entry.Entry.from_result(cur.column_names, res) for res in cur.fetchall()]


def get_all_projects_as_json() -> str:
    cur = db.conn.cursor()
    cur.execute(f"SELECT nr, name_ FROM {Project.Table.name}")
    result = {int(row[0]): row[1] for row in cur.fetchall()}
    cur.close()
    return json.dumps(result)


def calculate_worked_hours(empl_nr: int) -> float:
    cur = db.conn.cursor()
    command = f"SELECT SUM(TIMEDIFF(end_, start_)) FROM {entry.Entry.Table.name} " \
              f"where emplNr={empl_nr} AND end_ <= {util.date_to_sql(datetime.date.today() + datetime.timedelta(days=1))}"
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
    should_worked = count_work_days(empl.since, end) * decimal.Decimal(settings.get(settings.Names.SOLL_WORK_PER_DAY))
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


def collect_absences(empl_nr):
    cur = db.conn.cursor()
    command = f"SELECT * FROM {absence.Absence.Table.name} WHERE emplNr={empl_nr}"
    print(command)
    cur.execute(command)
    return [absence.Absence.from_result(cur.column_names, res) for res in cur.fetchall()]
