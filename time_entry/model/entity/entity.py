# coding=utf-8
import abc

from time_entry.model import db


class Entity(metaclass=abc):
    class Table(object):
        name: str
        sql_script: str

    @abc.abstractmethod
    def get_insert_command(self):
        pass

    @abc.abstractmethod
    def get_save_command(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def find(primary_key):
        pass

    @staticmethod
    @abc.abstractmethod
    def from_result(column_names, fetched):
        pass

    def save(self):
        cur = db.conn.cursor()
        cur.execute(self.get_save_command())

    def insert(self):
        cur = db.conn.cursor()
        cur.execute(self.get_insert_command())
