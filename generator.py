import json, re
import streamlit as st
from google import genai
from google.genai import types

class GeminiConfigError(Exception): pass
class GeminiGenerationError(Exception): pass

def secret(name, default=None):
    try: return st.secrets.get(name, default)
    except Exception: return default

def generate_questions(year, subject, chapter, count, qtypes, difficulty):
    api_key=secret("GEMINI_API_KEY")
    if not api_key:
        raise GeminiConfigError('API key missing. In Streamlit Cloud open Manage app → Settings → Secrets and add GEMINI_API_KEY = "your_key". Never put the key in GitHub.')
    model=secret("GEMINI_MODEL","gemini-3.8-flash")
    prompt=f"""
Act as an expert TG/AP Intermediate Mathematics question setter.
Create exactly {count} UNIQUE, mathematically meaningful questions.
Year: {year}
Subject: {subject}
Chapter: {chapter}
Allowed types: {", ".join(qtypes)}
Difficulty: {difficulty}
Language: English.

Rules:
- Stay within this chapter and Intermediate level.
- Do not claim questions are PYQs or add fake exam years.
- No duplicates or superficial number-only variations.
- Distribute requested types as evenly as possible.
- MCQ must have exactly four options labelled (A)-(D), one correct answer.
- Non-MCQ options must be [].
- Give correct final answers and detailed step-by-step solutions.
- If unsure, replace the question rather than guessing.
MATHEMATICAL FORMATTING RULES:
1. Write every mathematical expression in valid LaTeX.
2. Use \frac{}{} for fractions.
3. Use \sqrt{} for square roots.
4. Use ^{} for powers.
5. Use _{} for subscripts.
6. Use \int for integration.
7. Use \lim for limits.
8. Use \sum for summations.
9. Do not use plain-text approximations of mathematical equations.
10. Return equations as LaTeX strings.
Return JSON only:
{{"questions":[{{"type":"MCQ","question":"...","options":["(A) ...","(B) ...","(C) ...","(D) ..."],"answer":"...","solution":"...","difficulty":"Easy/Medium/Hard"}}]}}
Use only these types: {", ".join(qtypes)}.
"""
    try:
        client=genai.Client(api_key=api_key)
        response=client.models.generate_content(
            model=model, contents=prompt,
            config=types.GenerateContentConfig(temperature=0.45,response_mime_type="application/json")
        )
    except Exception as e:
        msg=str(e)
        if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
            raise GeminiGenerationError("Gemini free-tier request limit reached. Wait and try again, or check your Google AI Studio quota.")
        raise GeminiGenerationError("Gemini API request failed: "+msg)
    raw=(response.text or "").strip()
    raw=re.sub(r"^```(?:json)?\s*|\s*```$","",raw)
    a,b=raw.find("{"),raw.rfind("}")
    if a<0 or b<=a: raise GeminiGenerationError("Gemini did not return valid JSON. Please try again.")
    try: data=json.loads(raw[a:b+1])
    except Exception as e: raise GeminiGenerationError("Could not parse AI response: "+str(e))
    out=[]; seen=set()
    for q in data.get("questions",[]):
        if not isinstance(q,dict): continue
        typ=str(q.get("type","")).upper()
        question=str(q.get("question","")).strip()
        answer=str(q.get("answer","")).strip()
        solution=str(q.get("solution","")).strip()
        if typ not in qtypes or not question or not answer or not solution: continue
        key=re.sub(r"\W+","",question.lower())
        if key in seen: continue
        seen.add(key)
        opts=q.get("options",[])
        if typ=="MCQ":
            if not isinstance(opts,list) or len(opts)!=4: continue
            opts=[str(x) for x in opts]
        else: opts=[]
        level=str(q.get("difficulty","Medium")).title()
        if level not in ("Easy","Medium","Hard"): level="Medium"
        out.append({"type":typ,"question":question,"options":opts,"answer":answer,"solution":solution,"difficulty":level})
        if len(out)==count: break
    if len(out)<count:
        raise GeminiGenerationError(f"Gemini returned only {len(out)} valid unique questions out of {count}. No repeated filler questions were added. Try a smaller set or try again.")
    return out
