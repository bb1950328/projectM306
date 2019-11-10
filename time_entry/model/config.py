# coding=utf-8
import os

from time_entry.model.entity import setting


class Names(object):
    MAX_WORK_PER_DAY = "MAX_WORK_PER_DAY"
    SOLL_WORK_PER_DAY = "SOLL_WORK_PER_DAY"


def get(key: str) -> str:
    return setting.Setting.find(key).value


def set(key: str, value: str) -> None:
    se = setting.Setting.find(key)
    if se is None:
        se = setting.Setting()
        se.key = key
        se.value = value
        se.insert()
    se.value = value
    se.save()


def get_base_path():
    return os.path.abspath(os.path.join(__file__, ".."))
