# coding=utf-8


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
        employee.firstName = str(parts[1])
        employee.lastName = str(parts[2])
        return employee

    @staticmethod
    def validate_name(value):
        if ";" in value:
            raise ValueError("';' not allowed!")

    def _get_empl_nr(self) -> int:
        return self._empl_nr

    def _get_first_name(self) -> str:
        return self._first_name

    def _get_last_name(self) -> str:
        return self._last_name

    def _set_empl_nr(self, value) -> None:
        if value < 1:
            raise ValueError("emplNr must be 1 or greater!")
        self._empl_nr = value

    def _set_first_name(self, value) -> None:
        self.validate_name(value)
        self._first_name = value

    def _set_last_name(self, value) -> None:
        self.validate_name(value)
        self._last_name = value

    emplNr = property(_get_empl_nr, _set_empl_nr)
    firstName = property(_get_first_name, _set_first_name)
    lastName = property(_get_last_name, _set_last_name)
