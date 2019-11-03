# coding=utf-8
import datetime
from typing import Optional

import time_entry.model.entity.employee as employee
from time_entry.model import validate, model, util, db
from time_entry.model.entity.entity import Entity
from time_entry.model.entity.project import Project


class Entry(Entity):

    @staticmethod
    def from_result(column_names, fetched):
        def get(attr):
            return fetched[column_names.index(attr)]

        entry = Entry()
        entry.id = get("id")
        entry._emplNr = get("emplNr")
        entry._project_nr = get("projectNr")
        entry.start = get("start_")
        entry.end = get("end_")
        return entry

    @staticmethod
    def find(id):
        cur = db.conn.cursor()
        cur.execute(f"SELECT * FROM {Entry.Table.name} WHERE id={id}")
        return Entry.from_result(cur.column_names, cur.fetchone())

    def get_insert_command(self):
        sql_start = util.datetime_to_sql(self.start)
        sql_end = util.datetime_to_sql(self.end)
        return f"INSERT INTO {self.Table.name} (id, emplNr, projectNr, start_, end_) " \
               f"VALUES ((SELECT MAX(id) FROM {self.Table.name}), {self._empl_nr}, {self._project_nr}, " \
               f"{sql_start}, {sql_end})"

    def get_save_command(self):
        sql_start = util.datetime_to_sql(self.start)
        sql_end = util.datetime_to_sql(self.end)
        return f"UPDATE {self.Table.name} SET " \
               f"emplNr='{self._empl_nr}', projectNr='{self._project_nr}', start_={sql_start}, end_={sql_end}" \
               f"WHERE id={self.id}"

    _id: int
    _empl_nr: int
    _employee: Optional[employee.Employee]
    _project_nr: int
    _project: Optional[Project]
    _start: datetime.datetime
    _end: datetime.datetime

    class Table(object):
        name = "entry"
        sql_script = f"""create table {name}
                        (
                            id int not null,
                            emplNr int not null,
                            projectNr int not null,
                            start_ DATETIME not null,
                            end_ DATETIME not null,
                            constraint {name}_employee_emplNr_fk
                                foreign key (emplNr) references {employee.Employee.Table.name} (emplNr),
                            constraint {name}_project_nr_fk
                                foreign key (projectNr) references {Project.Table.name} (nr)
                        );
                        create unique index {name}_id_uindex
                            on {name} (id);
                        alter table {name}
                            add constraint {name}_pk
                                primary key (id);
                        """

    def getEmployee(self) -> employee.Employee:
        if not self._employee:
            self._employee = model.get_employee(self._empl_nr)
        return self._employee

    def getProject(self) -> Project:
        if not self._project:
            self._project = model.get_project(self._project_nr)
        return self._project

    def _set_id(self, id: int) -> None:
        validate.greater_than_0(id)
        self._id = id

    def _get_id(self) -> int:
        return self._id

    def _set_start(self, start: datetime.datetime):
        self._start = start

    def _get_start(self) -> datetime.datetime:
        return self._start

    def _set_end(self, end: datetime.datetime):
        self._end = end

    def _get_end(self) -> datetime.datetime:
        return self._end

    id = property(_get_id, _set_id)
    start = property(_get_start, _set_start)
    end = property(_get_end, _set_end)
