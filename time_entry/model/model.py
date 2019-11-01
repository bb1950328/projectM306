# coding=utf-8
import sqlite3

from time_entry.model import util
from time_entry.model.entity.employee import Employee
from time_entry.model.entity.project import Project

conn = sqlite3.connect(util.get_db_file_name(), detect_types=sqlite3.PARSE_DECLTYPES)

sqlite3.register_adapter(Employee, Employee.adapter)
sqlite3.register_adapter(Project, Project.adapter)

sqlite3.register_converter("EMPLOYEE", Employee.converter)
sqlite3.register_converter("PROJECT", Project.converter)


def get_employee(empl_nr):
    # TODO basil implement
    return None


def get_project(project_nr):
    # TODO basil implement
    return None
