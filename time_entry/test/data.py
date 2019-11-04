# coding=utf-8
import datetime

from time_entry.model.entity.employee import Employee
from time_entry.model.entity.entry import Entry
from time_entry.model.entity.project import Project

_generated = False

employees = []
projects = []
entries = []


def generate():
    global _generated
    if _generated:
        return

    employees_data = [[1, "Jan", "Kläger"],
                      [2, "Joel", "Suhner"],
                      [3, "Basil", "Bader"],
                      [4, "Marc", "Rusch"],
                      [5, "Quentin", "Weber"],
                      ]

    projects_data = [[1, "Test", "Dies ist wirklich nur ein Test"],
                     [2, "Modul226", "Java programmieren"],
                     [3, "Modul214", "Benutzer instruieren"],
                     [4, "Modul306", "IT-Kleinprojekte durchführen"],
                     [5, "Modul403", "Prozedurales programmieren mit C"],
                     ]

    entries_data = [[1, 1, datetime.datetime(2019, 10, 25, 7, 25, 0), datetime.datetime(2019, 10, 25, 11, 55, 30)],
                    [1, 2, datetime.datetime(2019, 10, 25, 13, 0, 0), datetime.datetime(2019, 10, 25, 16, 12, 59)],
                    [2, 3, datetime.datetime(2019, 10, 25, 13, 15, 0), datetime.datetime(2019, 10, 25, 17, 59, 59)],
                    [3, 3, datetime.datetime(2019, 10, 26, 8, 15, 0), datetime.datetime(2019, 10, 26, 12, 16, 17)],
                    [1, 1, datetime.datetime(2019, 10, 26, 3, 15, 0), datetime.datetime(2019, 10, 26, 12, 1, 17)],
                    [1, 1, datetime.datetime(2019, 10, 28, 14, 35, 0), datetime.datetime(2019, 10, 28, 18, 19, 17)],
                    ]

    for empl_nr, first_name, last_name in employees_data:
        empl = Employee()
        empl.emplNr = empl_nr
        empl.firstName = first_name
        empl.lastName = last_name
        employees.append(empl)

    for nr, name, desc in projects_data:
        proj = Project()
        proj.nr = nr
        proj.name = name
        proj.description = desc
        projects.append(proj)

    for empl_nr, project_nr, start, end in entries_data:
        en = Entry(project_nr, empl_nr)
        en._empl_nr = empl_nr
        en._project_nr = project_nr
        en.start = start
        en.end = end
        entries.append(en)

    _generated = True
