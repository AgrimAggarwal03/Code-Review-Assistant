# Zero-deploy fallback: Gemini Gem

If the Streamlit deploy fails, this still gives a valid prototype link.

1. Go to gemini.google.com, open Gems, create a new Gem named "Code Review Assistant".
2. In Instructions, paste the SYSTEM text from `prompts/final/P2_code_review.txt`.
3. Replace the "Return ONLY valid JSON" line with: "Format the answer with the headings Bugs, Style Issues, Hints, Test Cases."
4. Save, click Share, set access to "Anyone with the link", and copy the link.
5. Open the link in an incognito window and test it before submitting.
