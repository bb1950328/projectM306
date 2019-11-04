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
