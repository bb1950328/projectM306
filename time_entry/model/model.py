# coding=utf-8
import sqlite3

from time_entry.model import util

conn = sqlite3.connect(util.get_db_file_name(), detect_types=sqlite3.PARSE_DECLTYPES)
