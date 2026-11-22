"""Streamlit front end for the Code Review Assistant."""
import streamlit as st

from engine import run_pipeline

st.set_page_config(page_title="Code Review Assistant", page_icon="🧑‍🏫", layout="centered")
st.title("Code Review Assistant for Beginners")
st.caption(
    "Paste your code and get bugs, style tips, hints and test cases. "
    "You will not get the full solution, on purpose. Do not paste passwords, API keys or personal data."
)

language = st.selectbox("Language", ["auto", "python", "c++", "java", "c", "javascript"])
code = st.text_area("Your code", height=260, placeholder="Paste your code here...")
error_message = st.text_input("Error message you saw (optional)")

if st.button("Review my code", type="primary"):
    with st.spinner("Reviewing..."):
        try:
            result = run_pipeline(code, language, error_message or "none")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

    if result["status"] == "rejected":
        st.warning(result["message"])
        st.stop()

    if result["asked_for_solution"]:
        st.info("You asked for the full solution. This tool gives hints only, so here is a guided review instead.")

    r = result["review"]
    st.caption(f"Detected language: {result['language']}")
    st.success(r.get("summary", ""))

    st.subheader("Bugs")
    if r.get("bugs"):
        for b in r["bugs"]:
            line = f"Line {b['line']}: " if b.get("line") else ""
            st.markdown(f"**{line}{b.get('issue','')}**")
            st.markdown(f"Hint: {b.get('hint','')}")
    else:
        st.write("No bugs found.")

    st.subheader("Style issues")
    if r.get("style_issues"):
        for s in r["style_issues"]:
            line = f"Line {s['line']}: " if s.get("line") else ""
            st.markdown(f"**{line}{s.get('issue','')}**")
            st.markdown(f"Hint: {s.get('hint','')}")
    else:
        st.write("Style looks good.")

    st.subheader("Test cases")
    for t in r.get("test_cases", []):
        st.markdown(f"- Input: `{t.get('input','')}` → Expected: `{t.get('expected_output','')}`  \n  _{t.get('why','')}_")

    st.subheader("Your next step")
    st.write(r.get("next_step", ""))

    with st.expander("Raw JSON (for evaluators)"):
        st.json(result)
