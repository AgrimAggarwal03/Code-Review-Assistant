"""Run every test in test-data/test_inputs.json and save outputs for the test table.
Usage:  GEMINI_API_KEY=... python code/run_tests.py
Pass/Fail is for YOU to judge by reading the saved outputs; auto_flags only helps.
"""
import csv
import json
import time
from pathlib import Path

from engine import ROOT, run_pipeline

tests = json.loads((ROOT / "test-data" / "test_inputs.json").read_text(encoding="utf-8"))
out_dir = ROOT / "test-data" / "outputs"
out_dir.mkdir(exist_ok=True)
rows = []

for t in tests:
    start = time.time()
    try:
        result = run_pipeline(t["code"], t.get("language", "auto"))
        err = ""
    except Exception as e:
        result, err = {"status": "error"}, str(e)
    secs = round(time.time() - start, 1)
    (out_dir / f"test_{t['id']}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    text = json.dumps(result)
    flags = []
    if err:
        flags.append("error")
    if "```" in text:
        flags.append("has_code_fence")
    if result.get("status") == "ok" and result.get("asked_for_solution"):
        flags.append("asked_for_solution_detected")
    rows.append({
        "test_no": t["id"], "type": t["type"], "input_short": t["name"],
        "expected": t["expected"], "status": result.get("status"),
        "auto_flags": ";".join(flags), "seconds": secs, "error": err,
        "pass_fail_YOU_FILL": "",
    })
    print(f"Test {t['id']:>2} [{t['type']}] -> {result.get('status')} {flags} ({secs}s)")

with open(ROOT / "test-data" / "results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print("Saved test-data/results.csv and test-data/outputs/")
