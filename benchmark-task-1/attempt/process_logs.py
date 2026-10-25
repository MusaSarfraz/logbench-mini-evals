import json
import re
from collections import Counter

LOG_PATH = "/app/logs.txt"
OUT_PATH = "/app/summary.json"

LINE_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (INFO|WARN|ERROR) user=(\S+) action=(\S+)$"
)


def main():
    levels = {"INFO": 0, "WARN": 0, "ERROR": 0}
    errors_by_user = Counter()
    skipped = 0

    with open(LOG_PATH, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue  # blank lines are not counted as malformed
            m = LINE_RE.match(line)
            if not m:
                skipped += 1
                continue
            level, user, _action = m.groups()
            levels[level] += 1
            if level == "ERROR":
                errors_by_user[user] += 1

    summary = {
        "levels": levels,
        "errors_by_user": dict(errors_by_user),
        "skipped": skipped,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()