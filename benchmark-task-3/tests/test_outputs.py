import json
from pathlib import Path

def test_summary_correct():
    data = json.loads(Path("/app/summary.json").read_text())
    assert data["levels"] == {"INFO": 3, "ERROR": 5, "WARN": 1}
    assert data["errors_by_user"] == {"sara": 2, "ali": 1, "bilal_99": 2}
    assert data["skipped"] == 4
    assert data["duplicates"] == 2
    assert data["out_of_order"] == 2