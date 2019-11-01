# coding=utf-8
import abc


class Entity(metaclass=abc):
    class Table(metaclass=abc):
        name: str
        sql_script: str

    @abc.abstractmethod
    def get_insert_command(self):
        pass

    @abc.abstractmethod
    def get_save_command(self):
        pass
