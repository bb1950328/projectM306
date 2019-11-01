# coding=utf-8


def greater_than_0(value):
    if value < 1:
        raise ValueError("value must be 1 or greater!")


def name(value):
    if ";" in value:
        raise ValueError("';' not allowed!")
