# Changelog (changes since Milestone 1)

Edit the dates to match when your team actually did each item. Evaluators check for dated entries.

## 2026-11-22
- Built the Streamlit app (`code/app.py`) and shared engine (`code/engine.py`).
- Split the baseline prompt into a 2-step pipeline: P1 input check, P2 code review.
- Added prompt versions: v1 (Milestone 1 baseline), v2 (JSON output), v3/final (hard rules, injection guard, worked example, temperature 0.2).
- Added 11 test inputs (5 normal, 4 edge, 2 invalid) and `run_tests.py`.
- Added README, .gitignore and the deploy notes.
- Updated the model to `gemini-3.8-flash` after `gemini-2.5-flash` returned 404 (no longer available to new users).
- Added retries with short waits for busy (503) responses, a fallback model, and a friendly "service busy" message in the app.
