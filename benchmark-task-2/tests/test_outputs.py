import json
from pathlib import Path

def test_summary_correct():
    data = json.loads(Path("/app/summary.json").read_text())
    assert data["levels"] == {"INFO": 2, "ERROR": 4, "WARN": 1}
    assert data["errors_by_user"] == {"sara": 2, "ali": 1, "bilal_99": 1}
    assert data["skipped"] == 5