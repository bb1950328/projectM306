# coding=utf-8

import time_entry.model as model
from time_entry.model.entity.entity import Entity


class Setting(Entity):
    MAX_WORK_PER_DAY = "MAX_WORK_PER_DAY"
    SOLL_WORK_PER_DAY = "SOLL_WORK_PER_DAY"

    @staticmethod
    def from_result(column_names, fetched):
        def get(attr):
            return fetched[column_names.index(attr)]

        se = Setting()
        se.key = get("key_")
        se.value = get("value")
        return se

    @staticmethod
    def find(key):
        cur = model.db.get_conn().cursor()
        query = f"SELECT * FROM {Setting.Table.name} WHERE key_='{key}'"
        cur.execute(query)
        return Setting.from_result(cur.column_names, cur.fetchone())

    @staticmethod
    def find_int_value(key) -> int:
        return Setting._find_and_convert(key, int)

    @staticmethod
    def find_float_value(key) -> float:
        return Setting._find_and_convert(key, float)

    @staticmethod
    def _find_and_convert(key, func):
        res_str = Setting.find(key).value
        try:
            return func(res_str)
        except ValueError:
            raise ValueError(f"Value \"{res_str}\" cannot be converted to an {func.__name__}!")

    def get_insert_command(self):
        return f"INSERT INTO {self.Table.name} (key_, value) VALUES " \
               f"('{self.key}', '{self.value}')"

    def get_save_command(self):
        return f"UPDATE {self.Table.name} SET value_='{self.value}' " \
               f"WHERE key='{self.key}'"

    _key: str
    _value: str

    class Table(object):
        name = "setting"
        sql_script = f"""
        create table {name}
        (
            key_ VARCHAR(255) not null,
            value VARCHAR(2047) not null
        );
        create unique index {name}_key_uindex
            on {name} (key_);
        alter table {name}
            add constraint {name}_pk
                primary key (key_);
        """

    def _get_key(self) -> str:
        return self._key

    def _get_value(self) -> str:
        return self._value

    def _set_key(self, key) -> None:
        model.validate.name(key)
        self._key = key

    def _set_value(self, value) -> None:
        model.validate.name(value)
        self._value = value

    key = property(_get_key, _set_key)
    value = property(_get_value, _set_value)
