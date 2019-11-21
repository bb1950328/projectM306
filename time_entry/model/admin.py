# coding=utf-8
import subprocess
from typing import List, Dict, Tuple

from time_entry.model import util


def parse_commit(commit: str) -> dict:
    lines = commit.splitlines()

    def findline(word: str):
        for i, line in enumerate(lines):
            if word in line:
                return i

    idx_hash = findline("commit")
    idx_hash = 0 if not idx_hash else idx_hash
    idx_author = findline("Author:")
    idx_date = findline("Date:")

    hash_ = lines[idx_hash].replace("commit", "").strip().split(" ")[0].strip()
    author = lines[idx_author].strip().split(":", 1)[1].strip().split(" ")[0]
    date = lines[idx_date].strip().split(":", 1)[1].strip()
    idx_max = max(idx_hash, idx_date, idx_author)

    message_lines = lines[idx_max + 1:]
    message_lines = map(str.strip, message_lines)
    message = " ".join(message_lines)
    return {
        "hash": util.strmaxlen(hash_, 9),
        "author": author,
        "date": date,
        "message": message,
    }


def get_git_log() -> List[Dict[str, str]]:
    log = subprocess.getoutput("git log -n 10")
    commits = log.split("\ncommit")
    return list(map(parse_commit, commits))


def git_pull() -> Tuple[bool, str]:
    exitcode, output = subprocess.getstatusoutput("git pull")
    return exitcode == 0, output
