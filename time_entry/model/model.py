# coding=utf-8
import datetime

from django.contrib.auth.models import User

import time_entry.model.entity.employee as employee
import time_entry.model.entity.entry as entry
from time_entry.model import db, util
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
