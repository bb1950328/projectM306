# coding=utf-8
from time_entry.model import validate
from time_entry.model.entity.entity import Entity


class Employee(Entity):
    def get_insert_command(self):
        return f"INSERT INTO {self.Table.name} (emplNr, firstName, lastName) VALUES " \
               f"({self.emplNr}, '{self.firstName}', '{self.lastName}')"

    def get_save_command(self):
        return f"UPDATE {self.Table.name} SET firstName='{self.firstName}', lastName='{self.lastName}' " \
               f"WHERE emplNr={self.emplNr}"

    _empl_nr: int
    _first_name: str
    _last_name: str

    class Table(object):
        name = "employee"
        sql_script = f"""
        create table {name}
        (
            emplNr int not null,
            firstName VARCHAR(255) not null,
            lastName VARCHAR(255) not null
        );
        create unique index {name}_emplNr_uindex
            on {name} (emplNr);
        alter table {name}
            add constraint {name}_pk
                primary key (emplNr);
        """

    @staticmethod
    def adapter(employee) -> str:
        return f"{employee.emplNr};{employee.firstName};{employee.lastName}"

    @staticmethod
    def converter(bytestring):
        parts = bytestring.split(b";")
        employee = Employee()
        employee.emplNr = int(parts[0])
        employee.firstName = parts[1].decode("UTF-8", "replace")
        employee.lastName = parts[2].decode("UTF-8", "replace")
        return employee

    def _get_empl_nr(self) -> int:
        return self._empl_nr

    def _get_first_name(self) -> str:
        return self._first_name

    def _get_last_name(self) -> str:
        return self._last_name

    def _set_empl_nr(self, empl_nr) -> None:
        validate.greater_than_0(empl_nr)
        self._empl_nr = empl_nr

    def _set_first_name(self, first_name) -> None:
        validate.name(first_name)
        self._first_name = first_name

    def _set_last_name(self, last_name) -> None:
        validate.name(last_name)
        self._last_name = last_name

    emplNr = property(_get_empl_nr, _set_empl_nr)
    firstName = property(_get_first_name, _set_first_name)
    lastName = property(_get_last_name, _set_last_name)
