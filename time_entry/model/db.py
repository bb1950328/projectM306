# coding=utf-8
import json
import logging
import os
import re
from typing import Optional

from django.contrib.auth.models import User
from mysql import connector
from mysql.connector import DatabaseError, MySQLConnection, ProgrammingError

import time_entry.model.entity.employee as employee
import time_entry.model.entity.entry as entry
import time_entry.model.entity.project as project
from time_entry.model import config
from time_entry.model.entity import setting, absence

logging.getLogger().setLevel(logging.DEBUG)
_conn: Optional[MySQLConnection] = None


def load_connect_params():
    settings_file_name = "database_settings.json"
    path = os.path.join(config.get_base_path(), "..", settings_file_name)
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise ValueError(f"Database config file not found. "
                         f"Please copy \"{settings_file_name}.default\" to \"{path}\"")
    with open(path) as f:
        return json.load(f)


class Const(object):
    connect_params = load_connect_params()

    database_name = connect_params["db_name"]
    del connect_params["db_name"]

    all_entities = [setting.Setting,
                    employee.Employee,
                    project.Project,
                    entry.Entry,
                    absence.Absence,
                    ]


def get_conn():
    global _conn
    if _conn is None or not _conn.is_connected() or _conn.database is None:
        try:
            _conn = connector.connect(database=Const.database_name,
                                      **Const.connect_params,
                                      )
            _conn.ping(True)
        except ProgrammingError:
            _conn = None
    return _conn


def drop_database(cursor=None):
    if cursor is None:
        cursor = get_conn().cursor()
    cursor.execute(f"DROP DATABASE {Const.database_name}")
    User.objects.all().delete()


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
            drop_database(cur)
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
