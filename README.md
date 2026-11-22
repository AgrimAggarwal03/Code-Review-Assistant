# Code Review Assistant for Beginner Programmers

Team: Caffeine addicts · Course: SCSE4041 Mini Project · Milestone 2

An AI assistant that reviews beginner code and returns bugs, style issues, hints and test cases
**without revealing the full solution**. It uses a 2-step prompt pipeline on Gemini.

## Team
| Enrollment | Name |
|---|---|
| S24CSEU2304 | Agrim Aggarwal (leader) |
| S24CSEU2335 | Kunal |
| S24CSEU2309 | Anany Dixit |
| S24CSEU2322 | Utkarsh Kumar |
| S24CSEU2333 | Shashank Mishra |
| S24CSEU2330 | Shivam Singh |

Prototype link: <PASTE YOUR LIVE APP LINK HERE>

## How it works
1. **P1 Input Check** (`prompts/final/P1_input_check.txt`): is it code? which language? does the student want the full answer?
2. **P2 Code Review** (`prompts/final/P2_code_review.txt`): returns structured JSON with summary, bugs, style issues, test cases, next step.
3. The app (`code/app.py`) shows the result as friendly sections.

## Run locally
```
pip install -r requirements.txt
export GEMINI_API_KEY=your-key      # Windows PowerShell: $env:GEMINI_API_KEY="your-key"
cd code
streamlit run app.py
```
Never commit your key. `.gitignore` already excludes `.streamlit/secrets.toml` and `.env`.

## Run the tests
```
cd code
python run_tests.py
```
Outputs go to `test-data/outputs/` and `test-data/results.csv`. Read each output and fill the Pass/Fail column yourself.

## Deploy (free)
Streamlit Community Cloud or Hugging Face Spaces (Streamlit SDK): point it at `code/app.py`,
and add `GEMINI_API_KEY` in the platform's **Secrets** settings. See `docs/DEPLOY.md`.

## Folder map
`prompts/` v1, v2, v3, final · `code/` app, engine, test runner · `test-data/` inputs and outputs · `docs/` diagrams and the M2 PDF · `CHANGELOG.md`
