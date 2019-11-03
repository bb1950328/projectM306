# coding=utf-8
import logging
import re

logging.getLogger().setLevel(logging.DEBUG)


def name_is_main():
    return __name__ == "__main__"


if name_is_main():
    import django

    django.setup()

import sys

from mysql import connector
from mysql.connector import DatabaseError

import time_entry.model.entity.employee as employee
import time_entry.model.entity.entity as entity
import time_entry.model.entity.entry as entry
import time_entry.model.entity.project as project

conn = None


class Const(object):
    database_name = "time_entry"

    connect_params = {
        "user": "root",
        "password": "root",
        "host": "localhost",
        "port": 3306,
    }

    all_entities = [employee.Employee,
                    project.Project,
                    entry.Entry,
                    ]


def connect_to_database():
    try:
        global conn
        conn = connector.connect(database=Const.database_name,
                                 **Const.connect_params,
                                 )
    except ValueError:
        conn = None


def setup_database(ignore_existing=True):
    local_conn = connector.connect(**Const.connect_params)
    cur = local_conn.cursor()
    already_exists = True
    db_name = Const.database_name
    try:
        cur.execute(f"USE {db_name}")
    except DatabaseError:
        already_exists = False
    if already_exists:
        if ignore_existing:
            logging.getLogger().warning("Because ignore_existing is true, the existing database is dropped")
            cur.execute(f"DROP DATABASE {db_name}")
        else:
            raise ValueError(f"Database {db_name} already exists!!")

    cur.execute(f"CREATE DATABASE {db_name}")
    cur.execute(f"USE {db_name}")

    commands = "\n".join(ent.Table.sql_script for ent in Const.all_entities)
    logging.getLogger().info("Executing the following sql script to create all the tables: " + commands)
    from mysql.connector.cursor import RE_SQL_SPLIT_STMTS
    nl_and_indent = re.compile(b"\\n\\s*")
    encoded = commands.encode(local_conn.python_charset)
    for statement in RE_SQL_SPLIT_STMTS.split(encoded):
        formatted = b"".join(nl_and_indent.split(statement))
        if formatted:
            print(formatted)
            cur.execute(statement)

    local_conn.commit()
    cur.close()
    connect_to_database()


def insert_test_data():
    from time_entry.test import data
    data.generate()
    map(entity.Entity.insert, data.employees + data.projects + data.entries)


if name_is_main():
    """
    This script is executable as standalone by passing the function names you want to call as args.
    """
    for command in sys.argv[1:]:
        globals()[command]()
