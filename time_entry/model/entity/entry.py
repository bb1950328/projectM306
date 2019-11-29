# coding=utf-8
import datetime
from typing import Optional

import time_entry.model.entity.employee as employee
from time_entry.model import validate, util, db, model, config
from time_entry.model.entity.entity import Entity
from time_entry.model.entity.project import Project
from time_entry.model.entity.setting import Setting


class Entry(Entity):

    def __init__(self, project_nr=None, empl_nr=None):
        self._project_nr = project_nr
        self._empl_nr = empl_nr
        self._employee = None
        self._project = None
        self._id = None
        self._start = None
        self._end = None

    @staticmethod
    def from_result(column_names, fetched):
        def get(attr):
            return fetched[column_names.index(attr)]

        entry = Entry(get("projectNr"), get("emplNr"))
        entry.id = get("id")
        entry.start = get("start_")
        entry.end = get("end_")
        return entry

    @staticmethod
    def find(id):
        cur = db.get_conn().cursor()
        cur.execute(f"SELECT * FROM {Entry.Table.name} WHERE id={id}")
        return Entry.from_result(cur.column_names, cur.fetchone())

    def get_insert_command(self):
        sql_start = util.datetime_to_sql(self.start)
        sql_end = util.datetime_to_sql(self.end)
        return f"INSERT INTO {self.Table.name} (id, emplNr, projectNr, start_, end_) " \
               f"VALUES (IFNULL((SELECT MAX(id) FROM {self.Table.name} as tmpTable), 0) + 1, " \
               f"{self._empl_nr}, {self._project_nr}, {sql_start}, {sql_end})"

    def get_save_command(self):
        sql_start = util.datetime_to_sql(self.start)
        sql_end = util.datetime_to_sql(self.end)
        return f"UPDATE {self.Table.name} SET " \
               f"emplNr={self._empl_nr}, projectNr={self._project_nr}, start_={sql_start}, end_={sql_end}" \
               f" WHERE id={self.id}"

    def collides_with(self, other, fromself=False):
        start_inside = self.start < other.start < self.end
        end_inside = self.start < other.end < self.end
        from_other = other.collides_with(self, fromself=True) if not fromself else False
        return start_inside or end_inside or from_other

    def validate(self):
        if self.start.date() != self.end.date():
            raise ValueError("[Von] und [Bis] müssen am gleichen Tag sein!")
        if self.start > self.end:
            raise ValueError("[Von] muss vor [Bis] sein!")
        for_today = model.collect_entries(self._empl_nr,
                                          self.start.replace(hour=0, minute=0, second=0),
                                          self.end.replace(hour=23, minute=59, second=59))
        if self.id:
            for_today = list(filter(lambda e: e.id != self.id, for_today))
        sum_work = self.end - self.start
        for en in for_today:
            sum_work += (en.end - en.start)
            if self.collides_with(en):
                raise ValueError(f"{self} kollidiert mit {en}")
        sum_work_hours = sum_work.total_seconds() / 3600
        max_work_per_day = Setting.find_float_value(Setting.MAX_WORK_PER_DAY)
        if sum_work_hours > max_work_per_day:
            raise ValueError(f"Sie dürfen am {self.start.strftime('%d.%m.%Y')} "
                             f"höchstens {max_work_per_day}h arbeiten!")
        if self.getProject() is None:
            raise ValueError(f"Das Projekt mit der Nummer {self._project_nr} existiert nicht!")

    _id: Optional[int]
    _empl_nr: Optional[int]
    _employee: Optional[employee.Employee]
    _project_nr: Optional[int]
    _project: Optional[Project]
    _start: Optional[datetime.datetime]
    _end: Optional[datetime.datetime]

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
            self._employee = employee.Employee.find(self._empl_nr)
        return self._employee

    def getProject(self) -> Project:
        if not self._project:
            self._project = Project.find(self._project_nr)
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

    def __str__(self):
        return f"[Erfassung von {self.start.isoformat(sep=' ')} bis {self.end.isoformat(sep=' ')} " \
               f"auf Projekt Nr. {self._project_nr} von Mitarbeiter Nr. {self._empl_nr}]"

    id = property(_get_id, _set_id)
    start = property(_get_start, _set_start)
    end = property(_get_end, _set_end)
