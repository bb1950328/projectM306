# coding=utf-8
import os

from time_entry.model.entity import setting


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
    return os.path.abspath(os.path.join(__file__, "..", ".."))


def get_example_data_folder():
    return os.path.join(get_base_path(), "example_data")
