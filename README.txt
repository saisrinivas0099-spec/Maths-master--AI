MATHS MASTER AI - STEP 1 STARTER WEBSITE

REQUIREMENTS
- Windows 10/11
- Python 3.10 or newer
- Internet connection for installing Python packages

RUN
1. Extract this ZIP file.
2. Install Python from https://www.python.org/downloads/
   During installation, tick "Add Python to PATH".
3. Open the extracted Maths_Master_AI folder.
4. Double-click run_windows.bat.
5. Wait for installation. Streamlit will open the website in your browser.
6. If it does not open automatically, visit http://localhost:8501

IMPORTANT MVP NOTES
- This is a starter prototype, not a complete syllabus-wide AI engine.
- The demo generator currently has real worked examples for a small number of topics.
- For other chapters it provides a clearly generic placeholder example.
- The current 50-question mode may repeat demo examples; it does not claim to create 50 unique validated questions.
- Step 2 will add a free-tier AI provider option, chapter-specific prompt templates, uniqueness checks, and stronger mathematical verification.
- Review every generated question and solution before using it in a test or DPP.

PROJECT FILES
app.py          Streamlit website interface
syllabus.py     Initial TG/AP Intermediate chapter list
generator.py    Demo question generator
exporter.py     PDF export
requirements.txt Python packages
run_windows.bat One-click Windows launcher
