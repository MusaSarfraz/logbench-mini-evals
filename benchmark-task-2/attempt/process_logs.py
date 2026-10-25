import json
import re
from datetime import datetime

LINE_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) +(\d{2}:\d{2}:\d{2}) +([A-Za-z]+) +user=(\S+) +action=(\S+)$"
)
ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}


def parse_line(line):
    """Return (level, user) for a valid line, otherwise None."""
    m = LINE_RE.match(line)
    if not m:
        return None
    date_s, time_s, level, user, _action = m.groups()
    try:
        datetime.strptime(f"{date_s} {time_s}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    level = level.upper()
    if level not in ALLOWED_LEVELS:
        return None
    return level, user.lower()


def main():
    levels = {}
    errors_by_user = {}
    skipped = 0

    with open("/app/logs.txt") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parsed = parse_line(line)
            if parsed is None:
                skipped += 1
                continue
            level, user = parsed
            levels[level] = levels.get(level, 0) + 1
            if level == "ERROR":
                errors_by_user[user] = errors_by_user.get(user, 0) + 1

    summary = {
        "levels": levels,
        "errors_by_user": errors_by_user,
        "skipped": skipped,
    }
    with open("/app/summary.json", "w") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()