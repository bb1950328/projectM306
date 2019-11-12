# coding=utf-8
import subprocess
from typing import List, Dict


def parse_commit(commit: str) -> dict:
    lines = commit.splitlines()
    hash_ = lines[0].replace("commit", "").strip().split(" ")[0].strip()
    author = lines[1].strip().split(":", 1)[1].strip()
    date = lines[2].strip().split(":", 1)[1].strip()
    return {
        "hash": hash_,
        "author": author,
        "date": date,
    }


def get_git_log() -> List[Dict[str, str]]:
    log = subprocess.getoutput("git log -n 10")
    commits = log.split("\ncommit")
    return list(map(parse_commit, commits))


def git_pull() -> bool:
    exitcode, output = subprocess.getstatusoutput("git pull")
    return exitcode == 0
