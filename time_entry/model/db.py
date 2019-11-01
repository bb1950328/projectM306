# coding=utf-8
from mysql import connector
from mysql.connector import DatabaseError

from time_entry.model.entity.employee import Employee
from time_entry.model.entity.entity import Entity
from time_entry.model.entity.entry import Entry
from time_entry.model.entity.project import Project


class Const(object):
    database_name = "time_entry"

    connect_params = {
        "user": "root",
        "password": "root",
        "host": "localhost",
        "port": 3306,
    }

    all_entities = [Employee,
                    Project,
                    Entry,
                    ]


conn = connector.connect(database=Const.database_name,
                         **Const.connect_params,
                         )


def setup_database(ignore_existing=False):
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
            cur.execute(f"DROP DATABASE {db_name}")
        else:
            raise ValueError(f"Database {db_name} already exists!!")

    for entity in Const.all_entities:
        cur.execute(entity.Table.sql_script)


def insert_test_data():
    pass  # TODO basil implement


def insert_entity(entity: Entity):
    cur = conn.cursor()
    cur.execute(entity.get_insert_command)
