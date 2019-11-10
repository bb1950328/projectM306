# coding=utf-8
import datetime

from time_entry.model import config
from time_entry.model.entity import setting, absence
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

    first_nov_2019 = datetime.date(2019, 11, 1)
    employees_data = [[1, "Jan", "Kläger", first_nov_2019, None],
                      [2, "Joel", "Suhner", first_nov_2019, None],
                      [3, "Basil", "Bader", first_nov_2019, None],
                      [4, "Marc", "Rusch", first_nov_2019, None],
                      [5, "Quentin", "Weber", first_nov_2019, datetime.date(2019, 12, 31)],
                      ]

    projects_data = [[1, "Test", "Dies ist wirklich nur ein Test"],
                     [2, "Modul226", "Java programmieren"],
                     [3, "Modul214", "Benutzer instruieren"],
                     [4, "Modul306", "IT-Kleinprojekte durchführen"],
                     [5, "Modul403", "Prozedurales programmieren mit C"],
                     ]

    entries_data = [[1, 1, datetime.datetime(2019, 11, 1, 7, 25, 0), datetime.datetime(2019, 11, 1, 11, 55, 30)],
                    [1, 2, datetime.datetime(2019, 11, 1, 13, 0, 0), datetime.datetime(2019, 11, 1, 16, 12, 59)],
                    [2, 3, datetime.datetime(2019, 11, 1, 13, 15, 0), datetime.datetime(2019, 11, 1, 17, 59, 59)],
                    [3, 3, datetime.datetime(2019, 11, 4, 8, 15, 0), datetime.datetime(2019, 11, 4, 12, 16, 17)],
                    [1, 1, datetime.datetime(2019, 11, 4, 3, 15, 0), datetime.datetime(2019, 11, 4, 12, 1, 17)],
                    [1, 1, datetime.datetime(2019, 11, 5, 14, 35, 0), datetime.datetime(2019, 11, 5, 18, 19, 17)],
                    ]

    settings_data = {config.Names.MAX_WORK_PER_DAY: "12",
                     config.Names.SOLL_WORK_PER_DAY: "8.4"}

    absences_data = [
        [2, datetime.date(2019, 11, 4), datetime.date(2019, 11, 4), "Krankheit"],
        [2, datetime.date(2019, 11, 7), datetime.date(2019, 11, 8), "Krankheit"],
        [4, datetime.date(2019, 11, 4), datetime.date(2019, 11, 8), "Sonstiges"],
    ]

    for key, value in settings_data.items():
        se = setting.Setting()
        se.key = key
        se.value = value
        entries.append(se)

    for empl_nr, first_name, last_name, since, until in employees_data:
        empl = Employee()
        empl.emplNr = empl_nr
        empl.firstName = first_name
        empl.lastName = last_name
        empl.since = since
        empl.until = until
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

    for empl_nr, start, end, reason in absences_data:
        ab = absence.Absence(empl_nr, reason)
        ab.start = start
        ab.end = end
        entries.append(ab)

    _generated = True
