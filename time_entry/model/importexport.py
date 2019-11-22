# coding=utf-8
import datetime
import os
import shutil
import tempfile
from typing import List

from django.contrib.auth.models import User
from django.core import serializers

from time_entry.model import db, config, util

DELIMITER = ";"


def import_file(path: str) -> None:
    with open(path, encoding="UTF-8") as f:
        columns = map(str.strip, f.readline().split(DELIMITER))
    tmp_folder = " /etc/mysql/"  #tempfile.gettempdir()
    file_name = os.path.basename(path)
    tmp_path = os.path.join(tmp_folder, file_name)
    shutil.copyfile(path, tmp_path)
    table_name = file_name.split(".")[0]
    query = f"LOAD DATA INFILE '{util.path_to_sql(tmp_path)}' " \
            f"INTO TABLE {table_name} " \
            f"FIELDS TERMINATED BY '{DELIMITER}' ENCLOSED BY '\"' " \
            f"LINES TERMINATED BY '\\r\\n' " \
            f"IGNORE 1 ROWS " \
            f"({', '.join(columns)})"
    print(query)
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0;")
    cur.execute(query)
    cur.execute("SET FOREIGN_KEY_CHECKS=1;")
    conn.commit()
    cur.close()
    os.remove(tmp_path)


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
    export_users(folder)
    set_folder_permissions(folder, 0o777)


def import_all_files(folder: str):
    # todo import/export usernames and passwords too
    db.drop_database()
    db.setup_database()
    folder = os.path.join(config.get_example_data_folder(), folder)
    files = os.listdir(folder)
    files = filter(lambda fn: fn.endswith(".csv"), files)
    for fl in files:
        fl = os.path.join(folder, fl)
        print(f"Importing: {fl}")
        import_file(fl)
    import_users(folder)


def get_all_exported_folders() -> List[str]:
    generator = os.walk(config.get_example_data_folder())
    try:
        return generator.send(None)[1]
    except StopIteration:
        return []


def export_users(folder: str) -> None:
    path = _get_user_file_path(folder)
    with open(path, "w") as f:
        serializers.serialize("xml", User.objects.all(), stream=f)


def import_users(folder: str) -> None:
    path = _get_user_file_path(folder)
    for user in serializers.deserialize("xml", open(path)):
        user.save()


def _get_user_file_path(folder):
    return os.path.join(config.get_example_data_folder(), folder, "users.xml")


def set_folder_permissions(folder: str, perm_code=0o777):
    for root, dirs, files in os.walk(folder):
        for d in dirs:
            os.chmod(os.path.join(root, d), perm_code)
        for f in files:
            os.chmod(os.path.join(root, f), perm_code)
    #if util.is_on_windows():
