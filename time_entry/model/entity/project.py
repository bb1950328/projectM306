# coding=utf-8
from time_entry.model import validate, db
from time_entry.model.entity.entity import Entity


class Project(Entity):

    @staticmethod
    def from_result(column_names, fetched):
        if fetched is None:
            return None

        def get(attr):
            return fetched[column_names.index(attr)]

        project = Project()
        project.nr = get("nr")
        project.name = get("name_")
        project.description = get("description_")
        return project

    @staticmethod
    def find(nr):
        cur = db.conn.cursor()
        cur.execute(f"SELECT * FROM {Project.Table.name} WHERE nr={nr}")
        return Project.from_result(cur.column_names, cur.fetchone())

    def get_insert_command(self):
        return f"INSERT INTO {self.Table.name} (nr, name_, description_) VALUES " \
               f"({self.nr}, '{self.name}', '{self.description}')"

    def get_save_command(self):
        return f"UPDATE {self.Table.name} SET name_='{self.name}', description_='{self.description}' " \
               f"WHERE nr={self.nr}"

    _nr: int
    _name: str
    _description: str

    class Table(object):
        name = "project"
        sql_script = f"""create table {name}
                        (
                            nr int not null,
                            name_ VARCHAR(255) not null,
                            description_ VARCHAR(1023) not null
                        );
                        create unique index {name}_name__uindex
                            on {name} (name_);
                        create unique index {name}_nr_uindex
                            on {name} (nr);
                        alter table {name}
                            add constraint {name}_pk
                                primary key (nr);"""

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
