"""Shared logic for the Code Review Assistant: prompt loading, Gemini calls, 2-step pipeline."""
import json
import os
import re
from pathlib import Path

from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parent.parent
PROMPT_DIR = ROOT / "prompts"
# Tried in order; a model that returns 404 NOT_FOUND (retired or unavailable) is skipped.
# Override the first choice with the REVIEW_MODEL environment variable.
MODELS = [m for m in (os.environ.get("REVIEW_MODEL"), "gemini-3.8-flash", "gemini-flash-latest") if m]
MODEL = MODELS[0]


def get_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


def load_prompt(path_in_prompts):
    """Return (system, user_template) from a file with ### SYSTEM and ### USER markers."""
    text = (PROMPT_DIR / path_in_prompts).read_text(encoding="utf-8")
    system_part, user_part = text.split("### USER")
    system = system_part.replace("### SYSTEM", "").strip()
    return system, user_part.strip()


def fill(template, **values):
    """Plain replace, so JSON braces inside prompts never break formatting."""
    for k, v in values.items():
        template = template.replace("{" + k + "}", str(v))
    return template


def parse_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    return json.loads(text)


def _call_once(model, system, user, temperature):
    key = get_api_key()
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set. See README.md.")
    client = genai.Client(api_key=key)
    resp = client.models.generate_content(
        model=model,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            temperature=temperature,
            response_mime_type="application/json",
        ),
    )
    return resp.text or ""


def call_llm(system, user, temperature=0.2):
    """Call the first available model from MODELS."""
    last_err = None
    for model in MODELS:
        try:
            return _call_once(model, system, user, temperature)
        except Exception as e:
            if "NOT_FOUND" in str(e) or "404" in str(e):
                last_err = e
                continue
            raise
    raise last_err


def call_json(system, user, temperature=0.2, retries=1):
    """Call the model and parse JSON; retry once if the JSON is broken."""
    last_err = None
    for _ in range(retries + 1):
        raw = call_llm(system, user, temperature)
        try:
            return parse_json(raw), raw
        except json.JSONDecodeError as e:
            last_err = e
    raise ValueError(f"Model returned invalid JSON twice: {last_err}")


def check_input(code, language):
    """Prompt P1: is this code, which language, does the student want the full answer?"""
    system, tmpl = load_prompt("final/P1_input_check.txt")
    data, _ = call_json(system, fill(tmpl, code=code, language=language), temperature=0.0)
    return data


def review_code(code, language, error_message="none"):
    """Prompt P2: structured beginner-friendly review."""
    system, tmpl = load_prompt("final/P2_code_review.txt")
    user = fill(tmpl, code=code, language=language, error_message=error_message or "none")
    data, _ = call_json(system, user, temperature=0.2)
    return data


def run_pipeline(code, language="auto", error_message="none"):
    """Full workflow. Returns a dict with status: ok | rejected."""
    if not code or not code.strip():
        return {"status": "rejected", "message": "Please paste some code first."}
    check = check_input(code, language)
    if not check.get("is_code"):
        return {
            "status": "rejected",
            "message": "That does not look like code. Paste a program and try again.",
            "check": check,
        }
    lang = check.get("detected_language") if language == "auto" else language
    review = review_code(code, lang, error_message)
    return {
        "status": "ok",
        "check": check,
        "language": lang,
        "review": review,
        "asked_for_solution": bool(check.get("wants_full_solution")),
    }