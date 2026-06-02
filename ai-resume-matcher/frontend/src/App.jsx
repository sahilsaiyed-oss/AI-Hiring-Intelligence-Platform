import React, { useState, useRef } from "react";
import axios from "axios";
import { 
  UploadCloud, Loader2, FileText, Sparkles, Check, X, 
  Lightbulb, Target, ArrowRight, Download, BarChart3 
} from "lucide-react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from "chart.js";
import { Doughnut, Bar } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

export default function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null); // Will store the JSON response
  const fileInputRef = useRef(null);

  // 🚀 API CALL (Direct JSON handling)
  const handleAnalyze = async () => {
    if (!resumeFile || !jobDescription) {
      alert("Please upload a resume and paste the job description.");
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

      // Backend returns JSON directly. We just set it.
      // res.data structure: { ATS_SCORE, BREAKDOWN, MATCHED_SKILLS, MISSING_SKILLS, FEEDBACK }
      setData(res.data);
    } catch (err) {
      console.error("API Error:", err);
      alert("Backend Connection Failed. Make sure server is running on http://127.0.0.1:8000");
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (s) => (s >= 75 ? "#10b981" : s >= 50 ? "#f59e0b" : "#ef4444");

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-100 font-sans p-4 md:p-10">
      
      {/* HEADER */}
      <nav className="max-w-7xl mx-auto flex justify-between items-center mb-12 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-2">
          <Sparkles className="text-blue-500 fill-blue-500" size={24} />
          <h1 className="text-2xl font-black tracking-tighter uppercase italic text-white">ATS Resume AI</h1>
        </div>
        <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest hidden md:block">AI Hiring Intelligence</span>
      </nav>

      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10">
        
        {/* LEFT PANEL: INPUTS */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-[#1e293b] p-6 rounded-3xl border border-slate-700/50 shadow-xl">
            <label className="text-[10px] font-black uppercase text-slate-400 mb-3 block tracking-widest text-center">Job Description</label>
            <textarea
              placeholder="Paste job requirements here..."
              className="w-full h-48 bg-[#0f172a] border border-slate-700 rounded-2xl p-4 text-sm text-slate-200 outline-none focus:ring-2 focus:ring-blue-500/40 transition-all resize-none mb-6"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />

            <div onClick={() => fileInputRef.current.click()} className="border-2 border-dashed border-slate-700 rounded-2xl p-10 text-center cursor-pointer hover:bg-[#0f172a] transition-all mb-6 group">
              <input type="file" ref={fileInputRef} className="hidden" accept=".pdf" onChange={(e) => setResumeFile(e.target.files[0])} />
              <UploadCloud size={32} className={`mx-auto mb-2 ${resumeFile ? 'text-blue-500' : 'text-slate-500'}`} />
              <p className="text-[10px] font-bold text-slate-400 truncate px-2">
                {resumeFile ? resumeFile.name : "CLICK TO UPLOAD RESUME"}
              </p>
            </div>

            <button onClick={handleAnalyze} disabled={loading} className="w-full py-4 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 text-white font-black rounded-2xl shadow-lg transition-all flex justify-center items-center gap-2 uppercase text-xs">
              {loading ? <Loader2 className="animate-spin" /> : <>Analyze Performance <ArrowRight size={16}/></>}
            </button>
          </div>
        </div>

        {/* RIGHT PANEL: DASHBOARD */}
        <div className="lg:col-span-8">
          {!data && !loading ? (
            <div className="h-full min-h-[500px] bg-[#1e293b]/30 rounded-[2.5rem] border-2 border-dashed border-slate-800 flex flex-col items-center justify-center p-20 text-slate-500">
              <Target size={60} className="mb-4 opacity-10" />
              <p className="font-black uppercase tracking-widest text-sm">Awaiting Analysis Data</p>
            </div>
          ) : loading ? (
            <div className="h-full min-h-[500px] bg-[#1e293b] rounded-[2.5rem] flex flex-col items-center justify-center p-20 text-blue-500">
              <Loader2 size={60} className="animate-spin mb-4" />
              <p className="font-black uppercase tracking-tighter text-xl animate-pulse text-center">Processing JSON Results...</p>
            </div>
          ) : (
            <div className="space-y-6 pb-10 animate-in fade-in duration-500">
              
              {/* TOP ROW: Visual Score & Breakdown */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-[#1e293b] p-8 rounded-[2.5rem] border border-slate-700/50 flex flex-col items-center shadow-xl">
                  <p className="text-[10px] font-black uppercase text-slate-400 mb-6 tracking-widest">Overall Match Score</p>
                  <div className="w-48 h-24 relative">
                    <Doughnut 
                      data={{
                        datasets: [{ 
                          data: [data?.ATS_SCORE || 0, 100 - (data?.ATS_SCORE || 0)], 
                          backgroundColor: [getScoreColor(data?.ATS_SCORE), "#0f172a"], 
                          borderWidth: 0, circumference: 180, rotation: 270 
                        }]
                      }} 
                      options={{ cutout: '85%', plugins: { legend: { display: false } } }} 
                    />
                    <div className="absolute bottom-0 inset-x-0 text-center text-5xl font-black" style={{ color: getScoreColor(data?.ATS_SCORE) }}>
                      {data?.ATS_SCORE}%
                    </div>
                  </div>
                </div>

                <div className="bg-[#1e293b] p-8 rounded-[2.5rem] border border-slate-700/50 shadow-xl">
                  <p className="text-[10px] font-black uppercase text-slate-400 mb-6 tracking-widest text-center">Metric Breakdown</p>
                  <div className="h-28">
                    <Bar 
                      data={{
                        labels: ['Skills', 'Role', 'Exp', 'Keys'],
                        datasets: [{ 
                          data: [
                            data?.BREAKDOWN?.Skills || 0, 
                            data?.BREAKDOWN?.Role || 0, 
                            data?.BREAKDOWN?.Experience || 0, 
                            data?.BREAKDOWN?.Keywords || 0
                          ], 
                          backgroundColor: '#3b82f6', borderRadius: 4 
                        }]
                      }} 
                      options={{ 
                        maintainAspectRatio: false, 
                        plugins: { legend: { display: false } },
                        scales: { 
                          y: { display: false }, 
                          x: { grid: { display: false }, ticks: { color: '#64748b', font: { size: 10, weight: 'bold' } } } 
                        } 
                      }} 
                    />
                  </div>
                </div>
              </div>

              {/* MIDDLE ROW: Skills Tagging */}
              <div className="bg-[#1e293b] p-8 rounded-[2.5rem] border border-slate-700/50 shadow-xl">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div>
                    <h4 className="text-xs font-bold text-green-500 mb-4 flex items-center gap-2 uppercase tracking-widest">
                      <Check size={14} /> Matched Skills
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {data?.MATCHED_SKILLS?.length > 0 ? data.MATCHED_SKILLS.map((skill, i) => (
                        <span key={i} className="px-3 py-1.5 bg-green-500/10 text-green-400 text-[10px] font-bold rounded-lg border border-green-500/20 uppercase">
                          {skill}
                        </span>
                      )) : <span className="text-slate-500 text-xs italic">No direct matches found</span>}
                    </div>
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-red-400 mb-4 flex items-center gap-2 uppercase tracking-widest">
                      <X size={14} /> Skills to Learn
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {data?.MISSING_SKILLS?.length > 0 ? data.MISSING_SKILLS.map((skill, i) => (
                        <span key={i} className="px-3 py-1.5 bg-red-500/10 text-red-400 text-[10px] font-bold rounded-lg border border-red-500/20 uppercase">
                          {skill}
                        </span>
                      )) : <span className="text-slate-500 text-xs italic">No major gaps detected</span>}
                    </div>
                  </div>
                </div>
              </div>

              {/* BOTTOM ROW: FEEDBACK */}
              <div className="bg-[#1e293b] p-8 rounded-[2.5rem] border border-slate-700/50 shadow-xl relative overflow-hidden">
                <Lightbulb size={120} className="absolute -right-8 -bottom-8 text-blue-500 opacity-5 -rotate-12" />
                <p className="text-[10px] font-black uppercase text-blue-500 mb-6 tracking-widest flex items-center gap-2">
                  <Target size={16} className="fill-blue-500" /> Actionable Strategy
                </p>
                <div className="space-y-4">
                  {data?.FEEDBACK?.split('\n').filter(line => line.trim().length > 3).map((line, i) => (
                    <div key={i} className="flex gap-4 p-4 bg-[#0f172a]/50 rounded-2xl border border-slate-700/30">
                      <Check className="text-blue-500 shrink-0" size={16} />
                      <p className="text-xs font-medium text-slate-300 italic leading-relaxed">
                        {line.replace(/•/g, "").trim()}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          )}
        </div>
      </main>
    </div>
  );
}