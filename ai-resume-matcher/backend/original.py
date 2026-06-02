'''import os
import re
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import fitz  # PyMuPDF
from groq import Groq

# ✅ LOAD ENV FIRST
load_dotenv()

# ✅ INIT CLIENT
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

# ✅ CORS (Frontend connect ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# 🔧 HELPER FUNCTIONS
# -------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# SKILL MAP
SKILL_MAP = {
    "selenium": ["automation testing", "webdriver"],
    "postman": ["api testing", "rest api"],
    "python": ["django", "flask", "fastapi"],
    "react": ["frontend", "reactjs"],
    "sql": ["mysql", "database"],
    "jira": ["bug tracking", "agile"],
    "testing": ["manual testing", "qa"]
}

# -------------------------------
# 🚀 MAIN ATS FUNCTION
# -------------------------------

def calculate_score(resume_text, job_description):

    resume = clean_text(resume_text)
    jd = clean_text(job_description)

    # ---------------- ROLE MATCH ----------------
    try:
        prompt = f"""
        Compare roles strictly.

        Resume: {resume[:800]}
        JD: {jd[:800]}

        If roles are different give low score.

        Output only number 0-100.
        """

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        role_score = int(re.search(r'\d+', res.choices[0].message.content).group())

    except:
        role_score = 40

    # ---------------- SKILL MATCH ----------------
    required_skills = [s for s in SKILL_MAP if s in jd]

    matched = []
    missing = []

    for skill in required_skills:
        if skill in resume or any(x in resume for x in SKILL_MAP[skill]):
            matched.append(skill)
        else:
            missing.append(skill)

    skill_score = (len(matched) / len(required_skills) * 100) if required_skills else 50

    # ---------------- FINAL SCORE ----------------
    final_score = int((skill_score * 0.5) + (role_score * 0.5))

    # HARD PENALTY
    if role_score < 50:
        final_score -= 30

    final_score = max(0, min(100, final_score))

    # ---------------- FEEDBACK ----------------
    try:
        feedback_prompt = f"""
        Score: {final_score}
        Missing skills: {missing}

        Give 3 short improvement points.
        """

        feedback = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": feedback_prompt}],
            temperature=0.3
        ).choices[0].message.content

    except:
        feedback = "Improve missing skills."

    return f"""
ATS_SCORE: {final_score}
MATCHED_SKILLS: {", ".join(matched) if matched else "None"}
MISSING_SKILLS: {", ".join(missing) if missing else "None"}
FEEDBACK: {feedback}
"""


# -------------------------------
# 🌐 ROUTES
# -------------------------------

@app.get("/")
def home():
    return {"message": "ATS Engine Running 🚀"}

@app.post("/match_resume")
async def match_resume(resume: UploadFile, job_description: str = Form(...)):
    
    file_bytes = await resume.read()
    resume_text = extract_text_from_pdf(file_bytes)

    result = calculate_score(resume_text, job_description)

    return {"result": result}'''





'''
import React, { useState, useRef } from "react";
import axios from "axios";
import { UploadCloud, Loader2, FileText, Sparkles, Check, X, Lightbulb, Target, ArrowRight } from "lucide-react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const fileInputRef = useRef(null);

  // 🧠 Parse backend response
  const parseResult = (text) => {
    const score = text.match(/ATS_SCORE:\s*(\d+)/i)?.[1] || 0;
    const matched = text.match(/MATCHED_SKILLS:\s*([\s\S]*?)(?=MISSING_SKILLS|FEEDBACK|$)/i)?.[1] || "";
    const missing = text.match(/MISSING_SKILLS:\s*([\s\S]*?)(?=FEEDBACK|$)/i)?.[1] || "";
    const feedback = text.match(/FEEDBACK:\s*([\s\S]*)/i)?.[1] || text;

    return {
      score: parseInt(score),
      matched: matched.split(",").map(s => s.trim()).filter(Boolean),
      missing: missing.split(",").map(s => s.trim()).filter(Boolean),
      feedback
    };
  };

  // 🚀 API CALL
  const handleAnalyze = async () => {
    if (!resumeFile || !jobDescription) {
      alert("Upload resume + paste job description");
      return;
    }

    setLoading(true);
    setData(null);

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jobDescription);

    try {
      const res = await axios.post("http://127.0.0.1:8000/match_resume", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      setData(parseResult(res.data.result));
    } catch (err) {
      alert("Backend Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getColor = (s) => (s >= 75 ? "#10b981" : s >= 50 ? "#f59e0b" : "#ef4444");

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      {/* HEADER */}
      <div className="max-w-6xl mx-auto flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-blue-600 flex items-center gap-2">
          <Sparkles /> ATS Resume AI
        </h1>
        <span className="text-xs text-gray-400">AI Hiring Intelligence</span>
      </div>

      <div className="grid md:grid-cols-2 gap-6 max-w-6xl mx-auto">
        
        {/* LEFT PANEL */}
        <div className="bg-white p-6 rounded-2xl shadow">
          <textarea
            placeholder="Paste Job Description..."
            className="w-full h-40 border rounded-xl p-3 mb-4"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />

          <div
            onClick={() => fileInputRef.current.click()}
            className="border-2 border-dashed p-6 rounded-xl text-center cursor-pointer mb-4"
          >
            <input
              type="file"
              ref={fileInputRef}
              className="hidden"
              accept=".pdf"
              onChange={(e) => setResumeFile(e.target.files[0])}
            />
            <FileText className="mx-auto mb-2 text-gray-400" />
            {resumeFile ? resumeFile.name : "Upload Resume"}
          </div>

          <button
            onClick={handleAnalyze}
            className="w-full bg-blue-600 text-white py-3 rounded-xl flex justify-center gap-2"
          >
            {loading ? <Loader2 className="animate-spin" /> : <>Analyze <ArrowRight /></>}
          </button>
        </div>

        {/* RIGHT PANEL */}
        <div className="bg-white p-6 rounded-2xl shadow">
          {!data && !loading && (
            <div className="text-center text-gray-400">
              <Target size={40} className="mx-auto mb-2" />
              Waiting for input
            </div>
          )}

          {loading && (
            <div className="text-center text-blue-600">
              <Loader2 className="animate-spin mx-auto mb-2" />
              Analyzing...
            </div>
          )}

          {data && (
            <>
              {/* SCORE */}
              <div className="text-center mb-6">
                <Doughnut
                  data={{
                    datasets: [{
                      data: [data.score, 100 - data.score],
                      backgroundColor: [getColor(data.score), "#e5e7eb"]
                    }]
                  }}
                  options={{ cutout: "80%" }}
                />
                <h2 className="text-3xl font-bold mt-2" style={{ color: getColor(data.score) }}>
                  {data.score}%
                </h2>
              </div>

              {/* SKILLS */}
              <div className="mb-4">
                <h3 className="font-bold mb-2">Matched Skills</h3>
                {data.matched.map(s => <span key={s} className="bg-green-100 px-2 py-1 m-1 inline-block rounded">{s}</span>)}
              </div>

              <div className="mb-4">
                <h3 className="font-bold mb-2">Missing Skills</h3>
                {data.missing.map(s => <span key={s} className="bg-red-100 px-2 py-1 m-1 inline-block rounded">{s}</span>)}
              </div>

              {/* FEEDBACK */}
              <div className="bg-black text-white p-4 rounded-xl">
                <h3 className="mb-2">AI Feedback</h3>
                <p className="text-sm whitespace-pre-wrap">{data.feedback}</p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}'''