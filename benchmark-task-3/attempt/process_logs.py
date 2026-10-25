import json
import re
from collections import Counter
from datetime import datetime


LINE_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) "
    r"(\d{2}:\d{2}:\d{2}) "
    r"(INFO|WARN|ERROR) "
    r"user=([^\s=]+) "
    r"action=([^\s=]+)$",
    re.IGNORECASE,
)


def main():
    levels = Counter()
    errors_by_user = Counter()
    skipped = 0
    duplicates = 0
    out_of_order = 0

    seen = set()
    latest_timestamp = None

    with open("/app/logs.txt", "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line:
                continue

            match = LINE_PATTERN.fullmatch(line)

            if match is None:
                skipped += 1
                continue

            date_str, time_str, level, user, action = match.groups()

            try:
                timestamp = datetime.strptime(
                    f"{date_str} {time_str}",
                    "%Y-%m-%d %H:%M:%S",
                )
            except ValueError:
                skipped += 1
                continue

            level = level.upper()
            user = user.lower()

            key = (timestamp, level, user, action)

            if key in seen:
                duplicates += 1
                continue

            if (
                latest_timestamp is not None
                and timestamp < latest_timestamp
            ):
                out_of_order += 1
                continue

            seen.add(key)

            if (
                latest_timestamp is None
                or timestamp > latest_timestamp
            ):
                latest_timestamp = timestamp

            levels[level] += 1

            if level == "ERROR":
                errors_by_user[user] += 1

    summary = {
        "levels": dict(sorted(levels.items())),
        "errors_by_user": dict(sorted(errors_by_user.items())),
        "skipped": skipped,
        "duplicates": duplicates,
        "out_of_order": out_of_order,
    }

    with open("/app/summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()