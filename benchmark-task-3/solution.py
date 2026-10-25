import json
import re
from datetime import datetime

LINE_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(INFO|WARN|ERROR)"
    r"\s+user=(\S+)\s+action=(\S+)$",
    re.IGNORECASE,
)

def main():
    levels = {}
    errors_by_user = {}
    skipped = duplicates = out_of_order = 0
    seen = set()
    latest = None

    with open("/app/logs.txt") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            m = LINE_RE.match(line)
            if not m:
                skipped += 1
                continue
            try:
                ts = datetime.strptime(f"{m.group(1)} {m.group(2)}", "%Y-%m-%d %H:%M:%S")
            except ValueError:
                skipped += 1
                continue

            level = m.group(3).upper()
            user = m.group(4).lower()
            action = m.group(5)
            key = (ts, level, user, action)

            if key in seen:
                duplicates += 1
                continue
            if latest is not None and ts < latest:
                out_of_order += 1
                continue

            seen.add(key)
            latest = ts
            levels[level] = levels.get(level, 0) + 1
            if level == "ERROR":
                errors_by_user[user] = errors_by_user.get(user, 0) + 1

    with open("/app/summary.json", "w") as f:
        json.dump(
            {
                "levels": levels,
                "errors_by_user": errors_by_user,
                "skipped": skipped,
                "duplicates": duplicates,
                "out_of_order": out_of_order,
            },
            f,
        )

if __name__ == "__main__":
    main()