# coding=utf-8
import datetime
import os
from typing import List

from time_entry.model import db, config, util

DELIMITER = ";"


def import_file(path: str) -> None:
    with open(path, encoding="UTF-8") as f:
        columns = map(str.strip, f.readline().split(DELIMITER))
    table_name = os.path.basename(path).split(".")[0]
    query = f"LOAD DATA INFILE '{util.path_to_sql(path)}' " \
            f"INTO TABLE {table_name} " \
            f"FIELDS TERMINATED BY '{DELIMITER}' ENCLOSED BY '\"' " \
            f"LINES TERMINATED BY '\\r\\n' " \
            f"IGNORE 1 ROWS " \
            f"({', '.join(columns)})"
    print(query)
    cur = db.get_conn().cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0;")
    cur.execute(query)
    cur.execute("SET FOREIGN_KEY_CHECKS=1;")
    cur.close()


def to_str(obj: object) -> str:
    if obj is None:
        return "\\N"
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return '"' + obj.isoformat() + '"'
    return f'"{obj}"'


def export_table(path: str) -> None:
    table_name = os.path.basename(path).split(".")[0]
    cur = db.get_conn().cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    with open(path, "w", encoding="UTF-8") as f:
        f.write(DELIMITER.join(cur.column_names) + "\n")
        for row in cur.fetchall():
            line = DELIMITER.join(map(to_str, row))
            f.write(line + "\n")


def export_all_tables(folder: str):
    folder = os.path.join(config.get_example_data_folder(), folder)
    os.makedirs(folder, exist_ok=True)
    for en in db.Const.all_entities:
        table_name = en.Table.name
        path = os.path.join(folder, table_name + ".csv")
        print(f"Export {en} to {path}")
        export_table(path)


def import_all_files(folder: str):
    # todo import/export usernames and passwords too
    db.drop_database()
    db.setup_database()
    folder = os.path.join(config.get_example_data_folder(), folder)
    files = os.listdir(folder)
    for fl in files:
        fl = os.path.join(folder, fl)
        print(f"Importing: {fl}")
        import_file(fl)


def get_all_exported_folders() -> List[str]:
    generator = os.walk(config.get_example_data_folder())
    return generator.send(None)[1]
