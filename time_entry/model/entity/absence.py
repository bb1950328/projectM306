# coding=utf-8
import datetime
from typing import Optional

import time_entry.model.entity.employee as employee
from time_entry.model import validate, util, db, model
from time_entry.model.entity.entity import Entity
from time_entry.model.entity.project import Project


class Absence(Entity):

    def __init__(self, empl_nr=None, reason=None):
        self._empl_nr = empl_nr
        self._reason = reason
        self._employee = None
        self._id = None
        self._start = None
        self._end = None

    @staticmethod
    def from_result(column_names, fetched):
        def get(attr):
            return fetched[column_names.index(attr)]

        ab = Absence(get("empl_nr"), get("reason"))
        ab.id = get("id")
        ab.start = get("start_")
        ab.end = get("end_")
        return ab

    @staticmethod
    def find(id):
        cur = db.conn.cursor()
        cur.execute(f"SELECT * FROM {Absence.Table.name} WHERE id={id}")
        return Absence.from_result(cur.column_names, cur.fetchone())

    def get_insert_command(self):
        sql_start = util.date_to_sql(self.start)
        sql_end = util.date_to_sql(self.end)
        return f"INSERT INTO {self.Table.name} (id, emplNr, reason, start_, end_) " \
               f"VALUES (IFNULL((SELECT MAX(id) FROM {self.Table.name} as tmpTable), 0) + 1, " \
               f"{self._empl_nr}, '{self._reason}', {sql_start}, {sql_end})"

    def get_save_command(self):
        sql_start = util.date_to_sql(self.start)
        sql_end = util.date_to_sql(self.end)
        return f"UPDATE {self.Table.name} SET " \
               f"emplNr='{self._empl_nr}', reason='{self._reason}', start_={sql_start}, end_={sql_end}" \
               f" WHERE id={self.id}"

    def collides_with(self, other, fromself=False):
        start_inside = self.start < other.start < self.end
        end_inside = self.start < other.end < self.end
        from_other = other.collides_with(self, fromself=True) if not fromself else False
        return start_inside or end_inside or from_other

    def validate(self):
        if self.start > self.end:
            raise ValueError("[Von] muss vor [Bis] sein!")
        all_absences = model.collect_absences(self._empl_nr)
        for en in all_absences:
            if self.collides_with(en):
                raise ValueError(f"{self} kollidiert mit {en}")

    _id: Optional[int]
    _empl_nr: Optional[int]
    _employee: Optional[employee.Employee]
    _project_nr: Optional[int]
    _project: Optional[Project]
    _start: Optional[datetime.date]
    _end: Optional[datetime.date]

    class Table(object):
        name = "absence"
        sql_script = f"""create table {name}
                        (
                            id int not null,
                            emplNr int not null,
                            reason VARCHAR(255) not null,
                            start_ DATE not null,
                            end_ DATE not null,
                            constraint {name}_employee_emplNr_fk
                                foreign key (emplNr) references {employee.Employee.Table.name} (emplNr)
                        );
                        create unique index {name}_id_uindex
                            on {name} (id);
                        alter table {name}
                            add constraint {name}_pk
                                primary key (id);
                        """

    def getEmployee(self) -> employee.Employee:
        if not self._employee:
            self._employee = employee.Employee.find(self._empl_nr)
        return self._employee

    def _set_id(self, id: int) -> None:
        validate.greater_than_0(id)
        self._id = id

    def _get_id(self) -> int:
        return self._id

    def _set_start(self, start: datetime.date):
        self._start = start

    def _get_start(self) -> datetime.date:
        return self._start

    def _set_end(self, end: datetime.date):
        self._end = end

    def _get_end(self) -> datetime.date:
        return self._end

    def _set_reason(self, reason: str):
        self._reason = reason

    def _get_reason(self) -> str:
        return self._reason

    def __str__(self):
        return f"[Absenz von {util.locale_format(self.start)} bis {util.locale_format(self.end)} " \
               f"von Mitarbeiter Nr. {self._empl_nr} Grund:\"{self.reason}\"]"

    id = property(_get_id, _set_id)
    start = property(_get_start, _set_start)
    end = property(_get_end, _set_end)
    reason = property(_get_reason, _set_reason)
