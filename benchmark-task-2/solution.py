import json
import re
from datetime import datetime

LINE_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(INFO|WARN|ERROR)"
    r"\s+user=(\S+)\s+action=(\S+)$",
    re.IGNORECASE,
)

def real_datetime(date, time):
    try:
        datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def main():
    levels = {}
    errors_by_user = {}
    skipped = 0

    with open("/app/logs.txt") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            m = LINE_RE.match(line)
            if not m or not real_datetime(m.group(1), m.group(2)):
                skipped += 1
                continue

            level = m.group(3).upper()
            user = m.group(4).lower()
            levels[level] = levels.get(level, 0) + 1
            if level == "ERROR":
                errors_by_user[user] = errors_by_user.get(user, 0) + 1

    with open("/app/summary.json", "w") as f:
        json.dump(
            {"levels": levels, "errors_by_user": errors_by_user, "skipped": skipped},
            f,
        )

if __name__ == "__main__":
    main()