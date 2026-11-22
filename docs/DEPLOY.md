# Deploy on Streamlit Community Cloud (free)

1. Push this folder to a public GitHub repository (check no API key is inside any file).
2. Go to share.streamlit.io, sign in with GitHub, click Create app.
3. Choose your repo, branch main, main file path `code/app.py`.
4. Open Advanced settings, Secrets, and paste: `GEMINI_API_KEY = "your-key"`
5. Deploy. Copy the app URL: that is your Prototype link (Q11).
6. Test in an incognito window.

Get a free key at aistudio.google.com/apikey. Free-tier limits are low, so do not run the test script many times right before the demo.

Note: `requirements.txt` must be at the repo root, as it is here.
