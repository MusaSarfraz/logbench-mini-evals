import json

VALID_LEVELS = {"INFO", "WARN", "ERROR"}

def main():
    levels = {}
    errors_by_user = {}
    skipped = 0

    with open("/app/logs.txt") as f:
        for line in f:
            if not line.strip():
                continue  # ignore blank lines entirely

            parts = line.split()
            valid = (
                len(parts) == 5
                and parts[2] in VALID_LEVELS
                and parts[3].startswith("user=")
                and parts[4].startswith("action=")
            )

            if not valid:
                skipped += 1
                continue

            level = parts[2]
            user = parts[3][len("user="):]

            levels[level] = levels.get(level, 0) + 1
            if level == "ERROR":
                errors_by_user[user] = errors_by_user.get(user, 0) + 1

    summary = {
        "levels": levels,
        "errors_by_user": errors_by_user,
        "skipped": skipped,
    }
    with open("/app/summary.json", "w") as f:
        json.dump(summary, f)

if __name__ == "__main__":
    main()