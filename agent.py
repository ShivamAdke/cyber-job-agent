"""
Cybersecurity Job Assistant Agent
Author: Shivam Arvind Adke
Description: AI-powered agent to search jobs, score ATS match,
             generate cover letters and recruiter emails.
"""

import anthropic
import json
import re
import os
from datetime import datetime

# Load .env file manually (no extra library needed)
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

load_env()

# ── Your Resume Data ──────────────────────────────────────────────
RESUME = {
    "name": "Shivam Arvind Adke",
    "email": "sadke42@tntech.edu",
    "location": "Cookeville, TN",
    "linkedin": "linkedin.com/in/shivam-a-986442a9",
    "github": "github.com/ShivamAdke",
    "title": "PhD Researcher | Security Analyst | SOC Engineer",
    "summary": (
        "PhD researcher at TTU specializing in AI-powered security analytics, "
        "SOC triage, threat intelligence, and cloud security. Building LLM-assisted "
        "detection tools and agentic workflows for faster incident response and "
        "explainable MITRE ATT&CK mapping."
    ),
    "skills": [
        "SIEM Triage", "Threat Modeling", "Vulnerability Scanning",
        "Phishing Defense", "IDS/IPS", "VPN", "Firewall Admin",
        "AWS CloudTrail", "AWS GuardDuty", "AWS IAM/S3", "Azure VMs",
        "Splunk", "Nessus", "OpenVAS", "Wireshark", "Snort", "Metasploit",
        "Python", "Bash", "PowerShell", "Git",
        "MITRE ATT&CK", "NIST 800-53", "ISO 27001", "CIS Benchmarks", "PCI-DSS",
        "LLM Analytics", "Prompt Engineering", "RAG", "NLP Classification",
    ],
    "experience": [
        {
            "role": "Teaching Assistant",
            "company": "Tennessee Technological University",
            "duration": "Jan 2026 – Present",
            "points": [
                "Guided students through security labs — Linux, networking, security tooling.",
                "Supported grading and office hours for Cybersecurity/CS courses.",
            ],
        },
        {
            "role": "Security Analyst",
            "company": "Games for Love (NGO)",
            "duration": "Jan 2025 – Jan 2026",
            "points": [
                "Conducted phishing & email-security awareness training.",
                "Developed guidelines to reduce credential compromise risk.",
                "Supported secure coding practices in game development.",
            ],
        },
        {
            "role": "Security Engineer",
            "company": "Softwaroid Informatics",
            "duration": "Nov 2018 – Jun 2022",
            "points": [
                "SIEM-based alert triage — log analysis and escalation.",
                "Vulnerability assessments with Nessus/OpenVAS.",
                "Firewall administration and rule reviews.",
                "Responded to phishing, malware, and access-control incidents.",
            ],
        },
    ],
    "education": [
        {"degree": "PhD Computer Science (Cybersecurity)", "school": "Tennessee Technological University", "year": "2026–2029"},
        {"degree": "M.S. Cybersecurity", "school": "DePaul University", "year": "2022–2024"},
        {"degree": "B.E. Electronics & Telecommunications", "school": "Savitribai Phule Pune University", "year": "2018"},
    ],
    "certifications": [
        "CompTIA SecurityX (CASP+)", "CompTIA PenTest+", "CompTIA Security+",
        "CompTIA Network Vulnerability Assessment Professional",
        "Stanford: Exploiting & Protecting Web Applications",
        "Active Directory Attacks Lab", "Tata Cybersecurity Simulation",
    ],
    "projects": [
        "Kavach — Rogue AP/Wi-Fi Attack Detection (Python)",
        "Threat Intelligence Aggregator (Python, Flask, SQLite)",
        "AWS CloudTrail Detection Pipeline (AWS + Python)",
        "Azure Phishing-to-Callback Simulation (Kali + MSFVenom)",
        "Mini-SIEM — Log Collection & Correlation Rules (Python)",
        "OT/ICS Lab — Modbus Traffic Analysis (Wireshark)",
    ],
}

# ── Sample Job Listings (replace with live API in production) ─────
SAMPLE_JOBS = [
    {
        "id": 1,
        "title": "Security Analyst Intern",
        "company": "CrowdStrike",
        "location": "Remote",
        "type": "Internship",
        "description": (
            "Looking for a security analyst intern with experience in SIEM tools, "
            "threat intelligence, incident response, and vulnerability scanning. "
            "Familiarity with MITRE ATT&CK framework, Python scripting, and cloud "
            "security (AWS/Azure) is a plus. Knowledge of EDR tools preferred."
        ),
        "recruiter_email": "recruiting@crowdstrike.com",
    },
    {
        "id": 2,
        "title": "SOC Analyst (Summer Intern)",
        "company": "Palo Alto Networks",
        "location": "Santa Clara, CA / Remote",
        "type": "Internship",
        "description": (
            "Join our SOC team as a summer intern. You will work on alert triage, "
            "log analysis, threat hunting, and incident documentation. Experience "
            "with Splunk, firewall administration, NIST frameworks, and scripting "
            "in Python or Bash required. Understanding of IDS/IPS systems is preferred."
        ),
        "recruiter_email": "careers@paloaltonetworks.com",
    },
    {
        "id": 3,
        "title": "Cloud Security Research Intern",
        "company": "Microsoft",
        "location": "Redmond, WA / Remote",
        "type": "Research Internship",
        "description": (
            "Research internship in cloud security. Work on detection engineering, "
            "Azure security posture, and AI-powered threat analytics. PhD students "
            "preferred. Skills needed: Python, Azure, security research, LLM/NLP "
            "for security applications, MITRE ATT&CK mapping."
        ),
        "recruiter_email": "university@microsoft.com",
    },
    {
        "id": 4,
        "title": "Cybersecurity PhD Research Intern",
        "company": "IBM Research",
        "location": "Remote",
        "type": "Research Internship",
        "description": (
            "IBM Research is seeking a PhD intern to work on AI-driven security "
            "analytics, explainable threat detection, and agentic security workflows. "
            "Experience with LLMs, RAG systems, SIEM tools, and security data analysis "
            "required. Publications or projects in AI+Security a strong plus."
        ),
        "recruiter_email": "ibm.research.intern@ibm.com",
    },
]


def search_jobs(keywords: str = "", job_type: str = "internship") -> list:
    """Search and filter jobs from the listing."""
    results = []
    keywords_lower = keywords.lower()
    for job in SAMPLE_JOBS:
        if job_type.lower() in job["type"].lower():
            if not keywords or any(
                kw in job["title"].lower() or kw in job["description"].lower()
                for kw in keywords_lower.split()
            ):
                results.append(job)
    return results


def ats_score(job: dict) -> dict:
    """Calculate ATS match score between resume and job description."""
    client = anthropic.Anthropic()
    prompt = f"""
You are an ATS (Applicant Tracking System) analyzer.

Analyze the match between this resume and job description.
Return a JSON object with exactly these fields:
{{
  "score": <number 0-100>,
  "matched_skills": [<list of matched skills>],
  "missing_skills": [<list of important missing skills>],
  "verdict": "<Strong Match / Good Match / Partial Match / Weak Match>",
  "tip": "<one sentence improvement tip>"
}}

RESUME SKILLS: {json.dumps(RESUME["skills"])}
RESUME EXPERIENCE: {json.dumps([e["role"] + " at " + e["company"] for e in RESUME["experience"]])}
RESUME EDUCATION: {json.dumps([e["degree"] for e in RESUME["education"]])}
RESUME CERTS: {json.dumps(RESUME["certifications"])}

JOB TITLE: {job["title"]}
JOB COMPANY: {job["company"]}
JOB DESCRIPTION: {job["description"]}

Return ONLY valid JSON, no other text.
"""
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()
    # strip markdown fences if present
    raw = re.sub(r"^```json\s*|^```\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
    return json.loads(raw)


def generate_cover_letter(job: dict) -> str:
    """Generate a personalized cover letter for the job."""
    client = anthropic.Anthropic()
    prompt = f"""
Write a professional, concise cover letter (max 300 words) for this cybersecurity job.

APPLICANT:
- Name: {RESUME["name"]}
- Current Role: PhD Researcher at Tennessee Technological University
- Email: {RESUME["email"]}
- Location: {RESUME["location"]}
- Key Skills: {", ".join(RESUME["skills"][:12])}
- Top Projects: {", ".join(RESUME["projects"][:3])}
- Certifications: {", ".join(RESUME["certifications"][:3])}
- Summary: {RESUME["summary"]}

JOB:
- Title: {job["title"]}
- Company: {job["company"]}
- Location: {job["location"]}
- Description: {job["description"]}

Write a compelling cover letter. Be specific, confident, and highlight relevant experience.
Start directly with "Dear Hiring Manager," — no subject line needed.
"""
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def generate_recruiter_email(job: dict) -> str:
    """Generate a short cold outreach email to the recruiter."""
    client = anthropic.Anthropic()
    prompt = f"""
Write a short, professional cold outreach email (max 150 words) to a recruiter.

APPLICANT:
- Name: {RESUME["name"]}
- Role: PhD CS (Cybersecurity) Researcher at TTU
- LinkedIn: {RESUME["linkedin"]}
- GitHub: {RESUME["github"]}
- Email: {RESUME["email"]}
- Top Skills: SIEM, Threat Intel, Cloud Security, Python, MITRE ATT&CK, LLM Security

TARGET JOB:
- Title: {job["title"]}
- Company: {job["company"]}
- Recruiter Email: {job["recruiter_email"]}

Write a concise, friendly email with:
- Subject line (start with "Subject: ")
- Brief intro
- Why you're a great fit (2-3 points)
- Clear call to action
- Professional sign-off
"""
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def run_agent():
    """Main agent loop."""
    print("=" * 60)
    print("  🔐 Cybersecurity Job Assistant Agent")
    print(f"  👤 {RESUME['name']} | {RESUME['title']}")
    print("=" * 60)

    while True:
        print("\n📋 MENU")
        print("  1. Search Internships")
        print("  2. ATS Score — Match Resume to Job")
        print("  3. Generate Cover Letter")
        print("  4. Draft Recruiter Email")
        print("  5. Full Job Report (ATS + Cover Letter + Email)")
        print("  0. Exit")
        print("-" * 40)

        choice = input("Choose option: ").strip()

        if choice == "0":
            print("\n✅ Good luck with your internship search, Shivam!")
            break

        elif choice == "1":
            print("\n🔍 Searching cybersecurity internships...")
            jobs = search_jobs(keywords="security", job_type="internship")
            print(f"\nFound {len(jobs)} internship(s):\n")
            for j in jobs:
                print(f"  [{j['id']}] {j['title']}")
                print(f"       🏢 {j['company']} | 📍 {j['location']} | 🏷 {j['type']}")
                print()

        elif choice in ("2", "3", "4", "5"):
            jobs = search_jobs(keywords="security", job_type="internship")
            print("\nAvailable Jobs:")
            for j in jobs:
                print(f"  [{j['id']}] {j['title']} @ {j['company']}")
            job_id = input("\nEnter Job ID: ").strip()
            job = next((j for j in jobs if str(j["id"]) == job_id), None)
            if not job:
                print("❌ Invalid Job ID.")
                continue

            print(f"\n⚙️  Processing: {job['title']} @ {job['company']}...")

            if choice in ("2", "5"):
                print("\n📊 Calculating ATS Score...")
                result = ats_score(job)
                print(f"\n  Score     : {result['score']}/100  ({result['verdict']})")
                print(f"  Matched   : {', '.join(result['matched_skills'][:6])}")
                print(f"  Missing   : {', '.join(result['missing_skills'][:4])}")
                print(f"  Tip       : {result['tip']}")

            if choice in ("3", "5"):
                print("\n✉️  Generating Cover Letter...")
                letter = generate_cover_letter(job)
                filename = f"cover_letter_{job['company'].replace(' ', '_').lower()}.txt"
                with open(filename, "w") as f:
                    f.write(f"Cover Letter — {job['title']} @ {job['company']}\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(letter)
                print(f"\n  ✅ Saved to: {filename}")
                print("\n" + "-" * 40)
                print(letter[:400] + "..." if len(letter) > 400 else letter)
                print("-" * 40)

            if choice in ("4", "5"):
                print("\n📧 Drafting Recruiter Email...")
                email = generate_recruiter_email(job)
                filename = f"recruiter_email_{job['company'].replace(' ', '_').lower()}.txt"
                with open(filename, "w") as f:
                    f.write(f"Recruiter Email — {job['title']} @ {job['company']}\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(email)
                print(f"\n  ✅ Saved to: {filename}")
                print("\n" + "-" * 40)
                print(email)
                print("-" * 40)
        else:
            print("❌ Invalid option. Please choose 0-5.")


if __name__ == "__main__":
    run_agent()
