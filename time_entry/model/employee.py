# coding=utf-8
from time_entry.model import validate


class Employee(object):
    _empl_nr: int
    _first_name: str
    _last_name: str

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
