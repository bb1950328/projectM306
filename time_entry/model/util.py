# coding=utf-8
import datetime
import os
from typing import Optional, Union


def get_db_file_name():
    return os.path.abspath(os.path.join(__file__, "..", "..", "..", "db.sqlite3"))


def datetime_to_sql(value: datetime.datetime) -> str:
    return value.strftime("'%Y-%m-%d %H:%M:%S'")


def date_to_sql(value: Optional[datetime.date]) -> str:
    return value.strftime("'%Y-%m-%d'") if value else "NULL"


def path_to_sql(path: str) -> str:
    return path.replace("\\", "\\\\")


def is_work_day(day: Union[datetime.date, datetime.datetime]) -> bool:
    return day.isoweekday() <= 5  # 5 = friday


def locale_format(dt: Union[datetime.date, datetime.datetime, datetime.time]) -> str:
    date_fmt = "%d.%m.%Y"
    time_fmt = "%H:%M"
    if isinstance(dt, datetime.datetime):
        fmt = date_fmt + " " + time_fmt
    elif isinstance(dt, datetime.date):
        fmt = date_fmt
    else:
        fmt = time_fmt
    return dt.strftime(fmt)


def strmaxlen(inp: str, maxlen, dots=True):
    if len(inp) <= maxlen:
        return str
    if dots:
        maxlen -= 3
    new = inp[:maxlen]
    return new + "..." if dots else new


def is_on_windows():
    return os.name == 'nt'


def is_on_linux():
    return os.name == 'posix'


def repeat_maxlen(iterable, maxlen):
    colors = [*iterable]
    while len(colors) < maxlen:
        colors.extend(iterable)
    colors = colors[:maxlen]
    return colors
