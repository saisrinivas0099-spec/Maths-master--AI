MATHS MASTER AI - GEMINI UPDATE

A) Create API key:
1. Open https://aistudio.google.com/app/apikey
2. Sign in and create an API key.
3. Copy it privately. Never share it in chat or upload it to GitHub.

B) Update GitHub:
Upload and overwrite app.py, generator.py, syllabus.py, exporter.py and requirements.txt from this ZIP at the repository root. Commit changes.

C) Add Streamlit Secret:
Open Streamlit Community Cloud → your app → Manage app / Settings → Secrets.
Paste:
GEMINI_API_KEY = "PASTE_YOUR_KEY_HERE"
GEMINI_MODEL = "gemini-3.8-flash"
Save and allow the app to restart.

D) Test:
Open the deployed website, select year/subject/chapter/types/count and press Generate with Gemini AI.

NOTES:
- If gemini-3.8-flash is unavailable for your key, use a model name currently shown in Google AI Studio.
- Free tier, model availability and quotas can change. Check Google AI Studio pricing.
- Google's current pricing page says free-tier content may be used to improve products. Do not send confidential or personal data.
- Duplicate text and missing fields are filtered, but this is not mathematical proof of correctness. Have a subject expert verify all content before academic use.
