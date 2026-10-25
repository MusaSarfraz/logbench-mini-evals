import os, re
from pathlib import Path
from google import genai
import time
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

instruction = Path("instruction.md").read_text()
logs = Path("app/logs.txt").read_text()
script = Path("app/process_logs.py").read_text()

prompt = f"""{instruction}

Current /app/logs.txt:
{logs}

Current /app/process_logs.py:
{script}

Reply with ONLY the full corrected contents of process_logs.py in one python code block."""

resp = client.models.generate_content(
    model="gemini-3.8-flash",   # swap for whatever AI Studio lists now
    contents=prompt,
)

match = re.search(r"```python\n(.*?)```", resp.text, re.S)
code = match.group(1) if match else resp.text

resp = None
for attempt_no in range(5):
    try:
        resp = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        break
    except Exception as e:
        print(f"Try {attempt_no + 1} failed: {str(e)[:80]}")
        time.sleep(10 * (attempt_no + 1))

if resp is None:
    raise SystemExit("Model unavailable after 5 tries, run again later.")



Path("attempt").mkdir(exist_ok=True)
Path("attempt/process_logs.py").write_text(code, encoding="utf-8")
print("Saved attempt/process_logs.py")