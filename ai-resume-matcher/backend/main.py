import os
import re
import fitz  # PyMuPDF
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv

# 1. LOAD ENV & INIT GROQ
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

# 2. CORS (Frontend se connectivity ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. SMART SKILLS MAPPING
SKILL_MAP = {
    "python": ["django", "flask", "fastapi", "generators", "iterators", "data structures"],
    "sql": ["mysql", "postgresql", "database", "orm", "object relational mapping"],
    "react": ["frontend", "reactjs", "mobx", "ui", "user interface", "javascript"],
    "git": ["gitlab", "github", "version control", "svn", "mercurial"],
    "scripting": ["shell", "bash", "automation", "perl"],
    "architecture": ["multi-process", "scalable", "backend systems"]
}

# 4. HELPER: PDF TEXT EXTRACTION
def extract_text_from_pdf(file_bytes):
    try:
        # Fitz object opening from bytes
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

# 5. HELPER: SKILLS EXTRACTION LOGIC
def extract_skills_from_text(text):
    found = []
    text_lower = text.lower()
    for skill, synonyms in SKILL_MAP.items():
        # Check if main skill or any synonym exists
        if skill in text_lower or any(syn in text_lower for syn in synonyms):
            found.append(skill.upper())
    return list(set(found))

@app.post("/match_resume")
async def match_resume(resume: UploadFile = File(...), job_description: str = Form(...)):
    try:
        # A. Read PDF Bytes and Extract Text
        content = await resume.read()
        resume_text = extract_text_from_pdf(content)
        
        if not resume_text:
            return JSONResponse(status_code=400, content={"error": "Could not extract text from PDF"})

        # B. Skill Matching
        jd_skills = extract_skills_from_text(job_description)
        resume_skills = extract_skills_from_text(resume_text)

        matched = list(set(jd_skills) & set(resume_skills))
        missing = list(set(jd_skills) - set(resume_skills))

        # C. Role Match Logic (Using Groq)
        role_prompt = f"Resume: {resume_text[:1000]}\nJD: {job_description[:1000]}\nCompare the professional roles. Return ONLY a matching percentage number (0-100)."
        
        try:
            role_res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": role_prompt}],
                temperature=0.1
            )
            role_score_raw = re.findall(r'\d+', role_res.choices[0].message.content)
            role_score = int(role_score_raw[0]) if role_score_raw else 50
        except:
            role_score = 50

        # D. Calculate Scores
        skill_match_score = (len(matched) / len(jd_skills) * 100) if jd_skills else 80
        exp_score = 90 if any(word in resume_text.lower() for word in ["experience", "years", "present"]) else 60
        keyword_score = min(100, (len(resume_text.split()) / 200) * 100) # Basic depth check

        # Final Weighted Score
        ats_score = int((skill_match_score * 0.4) + (role_score * 0.3) + (exp_score * 0.15) + (keyword_score * 0.15))

        # E. AI Feedback (Using Groq)
        feedback_prompt = f"Resume Match: {ats_score}%. Matched Skills: {matched}. Missing: {missing}. Provide 3 short actionable bullet points to improve the resume."
        
        try:
            feedback_res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": feedback_prompt}],
                temperature=0.2
            )
            feedback = feedback_res.choices[0].message.content
        except:
            feedback = "Focus on highlighting technical skills and project metrics."

        # F. FINAL JSON RESPONSE (Matching your Frontend)
        return {
            "ATS_SCORE": ats_score,
            "BREAKDOWN": {
                "Skills": int(skill_match_score),
                "Role": int(role_score),
                "Experience": int(exp_score),
                "Keywords": int(keyword_score)
            },
            "MATCHED_SKILLS": matched,
            "MISSING_SKILLS": missing,
            "FEEDBACK": feedback
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def health():
    return {"status": "ATS Engine Active"}