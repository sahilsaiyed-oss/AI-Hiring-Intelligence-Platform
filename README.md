AI Hiring Intelligence Platform (ATS Pro)
The AI Hiring Intelligence Platform is a recruiter-grade Applicant Tracking System (ATS) designed to eliminate the inaccuracies of traditional keyword matchers. By utilizing a Hybrid Weighted Scoring Engine, it combines deterministic mathematical logic with semantic role analysis powered by the Groq LLaMA 3.1 model.
🚀 Key Value Proposition
Unlike most AI resume checkers that provide generic high scores (80%+), this platform enforces strict role-suitability checks. If a candidate's profile does not align with the professional domain of the job, the system applies a semantic penalty, ensuring only truly qualified candidates reach the top.
📸 Product Screenshots
1. Unified Entry Portal
The landing page features a clean, dark-themed dashboard where users can input job requirements and upload PDF resumes with ease.
![alt text](./screenshots/1.png)
2. Intelligent Match Analytics
Instant visualization of compatibility through a dynamic match gauge and category-specific breakdown bars (Skills, Role, Experience, and Keywords).
![alt text](./screenshots/2.png)
3. Actionable Strategy & Skill Gap
The system identifies exact matched skills and highlights missing competencies. It provides professional, non-generic AI feedback to help candidates optimize their profiles.
![alt text](./screenshots/3.png)
🔥 Core Features
Hybrid Scoring Algorithm: Uses a weighted formula (Skills 40%, Role 30%, Experience 15%, Keywords 15%) for realistic scoring.
Semantic Role Detection: Uses LLM (Groq) to understand if a "Python Developer" is actually suitable for a "QA Automation" role, applying penalties for domain mismatches.
Smart Skill Mapping: Automatically maps synonyms (e.g., recognizing that "PostgreSQL" satisfies a "SQL" requirement).
High-Performance PDF Parsing: Utilizes PyMuPDF (fitz) to extract clean text from binary PDF data.
Interactive Data Visualization: Integrated Chart.js for real-time Doughnut and Bar charts.
Professional PDF Reports: Ability to generate and download a comprehensive analysis report using jsPDF.
🛠️ Technology Stack
Frontend
Framework: React.js (Vite)
Styling: Tailwind CSS
Animations: Framer Motion
Charts: Chart.js (react-chartjs-2)
Icons: Lucide React
Backend
Framework: FastAPI (Python)
PDF Engine: PyMuPDF
Environment: Python Dotenv
AI / Machine Learning
Model: LLaMA-3.1-8B-Instant
API: Groq Cloud API
⚙️ Installation and Setup
1. Prerequisites
Python 3.10 or higher
Node.js 18.x or higher
A Groq API Key
2. Backend Installation
code
Bash
cd backend
python -m venv venv
# Activate venv
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
# Create .env and add GROQ_API_KEY=your_key
uvicorn main:app --reload
3. Frontend Installation
code
Bash
cd frontend
npm install
npm run dev
📂 Project Structure
code
Text
ai-resume-matcher/
├── screenshots/          # Application preview images
├── backend/
│   ├── main.py           # Logic Engine & FastAPI Endpoints
│   ├── .env              # API Configuration
│   └── requirements.txt  # Python Dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Dashboard UI & State Management
│   │   └── index.css     # Global Styles
│   └── package.json      # Dependencies & Scripts
└── README.md             # Project Documentation
🧪 Scoring Logic (The "Anti-Hallucination" Rule)
The system follows a strict mathematical model to prevent inflated AI scores:
Exact Match: When Resume Role == JD Role + High Skill Match → 85% - 100%
Partial Match: When Skills match but Role Domain differs slightly → 50% - 70%
Mismatch: When a different professional domain is detected → Score < 40% (Automatic Penalty)
🤝 Contact & Contribution
Built for the future of AI-driven recruitment.
Author: Sahil Saiyed
E-mail : sahilsaiyed067@gmail.com