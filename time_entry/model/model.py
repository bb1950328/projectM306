# coding=utf-8
from django.contrib.auth.models import User

from time_entry.model.entity.employee import Employee
from time_entry.model.entity.project import Project


def new_employee(empl_nr, first_name, last_name):
    em = Employee()
    em.emplNr = empl_nr
    em.firstName = first_name
    em.lastName = last_name
    em.insert()


def edit_employee(empl_nr, new_first_name=None, new_last_name=None):
    em = Employee.find(empl_nr)
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
