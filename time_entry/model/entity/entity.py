# coding=utf-8
import abc

from time_entry.model import db


class Entity(abc.ABC):
    class Table(abc.ABC):
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

    def validate(self):
        pass

    def save(self):
        self.validate()
        cur = db.get_conn().cursor()
        query = self.get_save_command()
        print(query)
        cur.execute(query)
        db.get_conn().commit()
        cur.close()

    def insert(self, connection=None):
        self.validate()
        if connection is None:
            connection = db.get_conn()
        cur = connection.cursor()
        command = self.get_insert_command()
        print(command)
        cur.execute(command)
        connection.commit()
        cur.close()
