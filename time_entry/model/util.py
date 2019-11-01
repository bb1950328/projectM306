# coding=utf-8
import datetime
import os


def get_db_file_name():
    return os.path.abspath(os.path.join(__file__, "..", "..", "..", "db.sqlite3"))


def datetime_to_sql(value: datetime.datetime) -> str:
    return value.strftime("'%Y-%m-%d %H:%M:%S'")
