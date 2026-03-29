# ET AI-Native News Experience
## Team Brain Stack — ET Gen AI Hackathon 2026

A **multi-agent AI system** that reimagines how business news is consumed.  
Built for **Problem Statement #8** of the Economic Times Gen AI Hackathon.

---

## 🤖 The 5 Agents

| Agent | What it does |
|-------|-------------|
| 📰 Personalization Agent | Ranks news by user role & interests |
| 🧠 Briefing Agent | Synthesizes N articles → 1 smart briefing |
| 📈 Story Arc Tracker | Builds timelines + sentiment arcs |
| 🌐 Vernacular Agent | Culturally adapts news in 4 Indian languages |
| 🎬 Video Script Agent | Turns articles into broadcast-ready scripts |

---

## 🚀 Quick Start (No Install Needed)

1. Open `demo/et_news_groq.html` in your browser
2. Get a free Groq API key at [console.groq.com/keys](https://console.groq.com/keys)
3. Paste your key in the bar at the top
4. Click any agent and see it work!

---

## 🛠️ Full Backend Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Groq API key
export GROQ_API_KEY=gsk_your_key_here   # Mac/Linux
set GROQ_API_KEY=gsk_your_key_here      # Windows

# 3. Run the backend
uvicorn backend.main:app --reload --port 8000

# 4. Open demo/et_news_groq.html in browser
```

---

## 📁 Project Structure

```
brain-stack-et-hackathon/
│
├── backend/
│   └── main.py              # FastAPI multi-agent backend
│
├── demo/
│   └── et_news_groq.html    # Single-file browser demo (no backend needed)
│
├── docs/
│   └── BrainStack_ET_Hackathon_Submission.pdf   # Official submission document
│   └── generate_pdf.py      # Script to regenerate the PDF
│
├── requirements.txt
└── README.md
```

---

## 🧠 Tech Stack

- **AI Engine:** Groq API + LLaMA 3.3 70B
- **Backend:** Python + FastAPI
- **Frontend:** HTML5 + CSS3 + Vanilla JS
- **Output Format:** Structured JSON from each agent

---

## 📄 Submission Document

See `docs/BrainStack_ET_Hackathon_Submission.pdf` for the full project documentation including architecture, problem statement, differentiation, and roadmap.

---

*Team Brain Stack — ET Gen AI Hackathon 2026*
