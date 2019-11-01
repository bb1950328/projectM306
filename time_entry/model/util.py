# coding=utf-8
import os


def get_db_file_name():
    return os.path.abspath(os.path.join(__file__, "..", "..", "..", "db.sqlite3"))
