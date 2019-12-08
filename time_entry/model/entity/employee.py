# coding=utf-8
import datetime
from typing import Set

import time_entry.model as model
from time_entry.model import db
from time_entry.model.entity.entity import Entity


class Role(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @staticmethod
    def of_name(name: str):
        for r in Role.ALL:
            if r.name == name:
                return r

    def __str__(self) -> str:
        return f"Role[{self.name}]"

    def __repr__(self) -> str:
        return f'Role("{self.name}", "{self.description}")'


Role.ADMIN = Role("admin", "Administrator")
Role.HR = Role("hr", "Human Resources Manager")
Role.CEO = Role("ceo", "Geschäftsleiter")
Role.BOSS = Role("boss", "Chef")
Role.EMPLOYEE = Role("employee", "Mitarbeiter")
Role.ALL = [  # todo prettier solution
    Role.ADMIN,
    Role.HR,
    Role.CEO,
    Role.BOSS,
    Role.EMPLOYEE,
]


class Permission(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @staticmethod
    def _in_employee(roles: Set[Role], employee) -> bool:
        return len(roles & employee.roles) > 0

    @staticmethod
    def can_view_employee_list(employee):
        required = {Role.ADMIN, Role.HR, Role.CEO, Role.BOSS}
        return Permission._in_employee(required, employee)

    @staticmethod
    def can_view_employee_details(employee):
        required = {Role.ADMIN, Role.HR, Role.CEO, Role.BOSS}
        return Permission._in_employee(required, employee)

    @staticmethod
    def can_edit_employee_details(employee):
        required = {Role.ADMIN, Role.HR, Role.CEO}
        return Permission._in_employee(required, employee)

    @staticmethod
    def can_add_absence(employee):
        required = {Role.ADMIN, Role.HR, Role.CEO}
        return Permission._in_employee(required, employee)

    @staticmethod
    def can_be_admin(employee):
        required = {Role.ADMIN}
        return Permission._in_employee(required, employee)

    @staticmethod
    def can_view_project_list(employee):
        required = {Role.ADMIN, Role.HR, Role.CEO, Role.BOSS}
        return Permission._in_employee(required, employee)

    @staticmethod
    def can_view_project_details(employee):
        required = {Role.ADMIN, Role.HR, Role.CEO, Role.BOSS}
        return Permission._in_employee(required, employee)


class Employee(Entity):

    def __init__(self) -> None:
        self._roles = set()

    def has_role(self, role: Role):
        return role.name in self.roles

    def insert(self, connection=None):
        super().insert(connection)
        model.model.add_user(str(self.emplNr), self.firstName)

    @staticmethod
    def from_result(column_names, fetched):
        def get(attr):
            return fetched[column_names.index(attr)]

        empl = Employee()
        empl.emplNr = get("emplNr")
        empl.firstName = get("firstName")
        empl.lastName = get("lastName")
        empl.since = get("since")
        empl.until = get("until")
        splitted = get("roles").split("+")
        if splitted[0]:
            empl.roles = {Role.of_name(x) for x in splitted}
        else:
            empl.roles = set()
        return empl

    @staticmethod
    def find(empl_nr):
        cur = db.get_conn().cursor()
        cur.execute(f"SELECT * FROM {Employee.Table.name} WHERE emplNr={empl_nr}")
        return Employee.from_result(cur.column_names, cur.fetchone())

    def get_insert_command(self):
        roles = "+".join([r.name for r in self.roles])
        return f"INSERT INTO {self.Table.name} (emplNr, firstName, lastName, since, until, roles) VALUES " \
               f"({self.emplNr}, '{self.firstName}', '{self.lastName}', " \
               f"{model.util.date_to_sql(self.since)}, {model.util.date_to_sql(self.until)}, '{roles}')"

    def get_save_command(self):
        roles = "+".join([r.name for r in self.roles])
        return f"UPDATE {self.Table.name} SET firstName='{self.firstName}', lastName='{self.lastName}', " \
               f"since={model.util.date_to_sql(self.since)}, until={model.util.date_to_sql(self.until)}, " \
               f"roles='{roles}' WHERE emplNr={self.emplNr}"

    _empl_nr: int
    _first_name: str
    _last_name: str
    _since: datetime.date
    _until: datetime.date
    _roles: Set[Role]

    class Table(object):
        name = "employee"
        sql_script = f"""
        create table {name}
        (
            emplNr int not null,
            firstName VARCHAR(255) not null,
            lastName VARCHAR(255) not null,
            roles VARCHAR(255) not null,
            since DATE not null,
            until DATE
        );
        create unique index {name}_emplNr_uindex
            on {name} (emplNr);
        alter table {name}
            add constraint {name}_pk
                primary key (emplNr);
        """

    def _get_empl_nr(self) -> int:
        return self._empl_nr

    def _get_first_name(self) -> str:
        return self._first_name

    def _get_last_name(self) -> str:
        return self._last_name

    def _get_since(self) -> datetime.date:
        return self._since

    def _get_until(self) -> datetime.date:
        return self._until

    def _set_empl_nr(self, empl_nr) -> None:
        model.validate.greater_than_0(empl_nr)
        self._empl_nr = empl_nr

    def _set_first_name(self, first_name) -> None:
        model.validate.name(first_name)
        self._first_name = first_name

    def _set_last_name(self, last_name) -> None:
        model.validate.name(last_name)
        self._last_name = last_name

    def _set_since(self, since: datetime.date) -> None:
        self._since = since

    def _set_until(self, until: datetime.date) -> None:
        self._until = until

    def _set_roles(self, roles: Set[Role]) -> None:
        self._roles = roles

    def _get_roles(self) -> set:
        return self._roles

    emplNr = property(_get_empl_nr, _set_empl_nr)
    firstName = property(_get_first_name, _set_first_name)
    lastName = property(_get_last_name, _set_last_name)
    since = property(_get_since, _set_since)
    until = property(_get_until, _set_until)
    roles = property(_get_roles, _set_roles)
