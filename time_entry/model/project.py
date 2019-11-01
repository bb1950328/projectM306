# coding=utf-8
from time_entry.model import validate


class Project(object):
    _nr: int
    _name: str
    _description: str

    @staticmethod
    def adapter(project) -> str:
        return f"{project.nr};{project.name};{project.description}"

    @staticmethod
    def converter(bytestring):
        parts = bytestring.split(b";")
        project = Project()
        project.nr = int(parts[0])
        project.name = parts[1].decode("UTF-8", "replace")
        project.description = parts[2].decode("UTF-8", "replace")
        return project

    def _set_nr(self, nr: int) -> None:
        validate.greater_than_0(nr)
        self._nr = nr

    def _set_name(self, name: str) -> None:
        validate.name(name)
        self._name = name

    def _set_description(self, description: str) -> None:
        validate.name(description)
        self._description = description

    def _get_nr(self) -> int:
        return self._nr

    def _get_name(self) -> str:
        return self._name

    def _get_description(self) -> str:
        return self._description

    nr = property(_get_nr, _set_nr)
    name = property(_get_name, _set_name)
    description = property(_get_description, _set_description)
