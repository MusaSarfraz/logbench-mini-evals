The script /app/process_logs.py reads /app/logs.txt and should write
/app/summary.json with exactly these keys:

- "levels": dict of how many valid log lines exist per level (INFO, WARN, ERROR)
- "errors_by_user": dict of how many ERROR lines each user has
- "skipped": the number of malformed lines that were ignored

A valid line looks like: DATE TIME LEVEL user=NAME action=ACTION
Any line that doesn't match that shape is malformed and must be skipped,
not counted.

Fix and extend the script so it runs correctly and produces the right
summary.json. Run it once so /app/summary.json exists.