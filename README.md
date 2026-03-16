# 🔐 Cybersecurity Job Assistant Agent

An AI-powered agent that helps cybersecurity professionals find internships, score ATS match, generate cover letters, and draft recruiter emails — all personalized to your resume.

Built by **Shivam Arvind Adke** | PhD Researcher, Tennessee Technological University

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Job Search | Search cybersecurity internships by keyword |
| 📊 ATS Score | Match your resume against any job description (0–100) |
| ✉️ Cover Letter | AI-generated, personalized cover letter per job |
| 📧 Recruiter Email | Cold outreach email drafted in seconds |
| 📁 Auto-save | All outputs saved as `.txt` files |

---

## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/ShivamAdke/cyber-job-agent.git
cd cyber-job-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key
```bash
# Linux / Mac
export ANTHROPIC_API_KEY="your-api-key-here"

# Windows
set ANTHROPIC_API_KEY=your-api-key-here
```
Get your free API key at: https://console.anthropic.com

### 4. Run the agent
```bash
python agent.py
```

---

## 🖥️ Usage

```
============================================================
  🔐 Cybersecurity Job Assistant Agent
  👤 Shivam Arvind Adke | PhD Researcher | Security Analyst
============================================================

📋 MENU
  1. Search Internships
  2. ATS Score — Match Resume to Job
  3. Generate Cover Letter
  4. Draft Recruiter Email
  5. Full Job Report (ATS + Cover Letter + Email)
  0. Exit
```

### Example Output — ATS Score
```
📊 ATS Score Result:
  Score   : 87/100  (Strong Match)
  Matched : SIEM, Python, MITRE ATT&CK, Threat Intel, AWS, Splunk
  Missing : EDR tools, Kubernetes
  Tip     : Add EDR experience (CrowdStrike Falcon) to boost score.
```

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Anthropic Claude API** (claude-haiku-4-5 — fast & cost-effective)
- No external dependencies beyond `anthropic`

---

## 📁 Project Structure

```
cyber-job-agent/
├── agent.py          # Main agent
├── requirements.txt  # Dependencies
└── README.md         # This file
```

Generated files (auto-created on run):
```
cover_letter_crowdstrike.txt
recruiter_email_microsoft.txt
...
```

---

## 🔧 Customization

Edit `RESUME` dict in `agent.py` to update your details.  
Edit `SAMPLE_JOBS` list to add real job postings.  
Connect to LinkedIn/Indeed API for live job search (roadmap).

---

## 📌 Roadmap

- [ ] Live job scraping via LinkedIn Jobs API
- [ ] Auto-save all outputs to PDF
- [ ] Web UI with Streamlit
- [ ] Multi-resume profile support

---

## 📄 License

MIT License — free to use and modify.

---


