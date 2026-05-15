from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import json
import numpy as np
import pdfplumber
import re
import io
import os
from groq import Groq
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ResumeIQ API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load Models ──────────────────────────────────────────
BASE = os.path.dirname(__file__)

with open(os.path.join(BASE, "models/tfidf_vectorizer.pkl"), "rb") as f:
    tfidf = pickle.load(f)

with open(os.path.join(BASE, "models/job_role_classifier.pkl"), "rb") as f:
    rf_bundle = pickle.load(f)
    rf        = rf_bundle["classifier"]
    role_enc  = rf_bundle["role_encoder"]

with open(os.path.join(BASE, "models/cosine_centroids.pkl"), "rb") as f:
    cos_bundle     = pickle.load(f)
    role_centroids = cos_bundle["centroids"]

with open(os.path.join(BASE, "models/placement_model.pkl"), "rb") as f:
    p_bundle       = pickle.load(f)
    place_pipeline = p_bundle["pipeline"]
    place_encoders = p_bundle["label_encoders"]
    place_features = p_bundle["features"]
    place_cat_cols = p_bundle["cat_cols"]
    place_cats     = p_bundle["categories"]

with open(os.path.join(BASE, "data/job_roles.json"), "r") as f:
    job_roles = json.load(f)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("✅ All models loaded!")

# ── Helpers ───────────────────────────────────────────────
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_pdf_text(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + " "
    return text.strip()

def match_jobs(resume_text, top_n=5):
    cleaned    = clean_text(resume_text)
    resume_vec = tfidf.transform([cleaned])
    resume_arr = np.asarray(resume_vec.todense())

    # Random Forest prediction
    rf_idx        = rf.predict(resume_vec)[0]
    rf_role       = role_enc.inverse_transform([rf_idx])[0]
    rf_confidence = round(float(rf.predict_proba(resume_vec)[0][rf_idx]) * 100, 2)

    # Cosine similarity ranking
    scores = {
        role: round(float(cosine_similarity(resume_arr, c)[0][0]) * 100, 2)
        for role, c in role_centroids.items()
    }
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    return {
        "primary_role":  rf_role,
        "rf_confidence": rf_confidence,
        "ranked_roles":  [{"role": r, "score": s} for r, s in ranked],
    }

def predict_placement(resume_text):
    text_lower = resume_text.lower()

    has_workex  = 1 if any(w in text_lower for w in ["experience", "worked", "internship", "company"]) else 0
    is_commerce = 1 if any(w in text_lower for w in ["commerce", "accounting", "finance", "bcom"]) else 0
    has_mba     = 1 if any(w in text_lower for w in ["mba", "management", "business administration"]) else 0

    degree_t       = "Comm&Mgmt" if is_commerce else "Sci&Tech"
    specialisation = "Mkt&Fin"   if has_mba     else "Mkt&HR"
    workex         = "Yes"       if has_workex  else "No"
    hsc_s          = "Commerce"  if is_commerce else "Science"

    inp = pd.DataFrame([{
        "ssc_p": 70, "hsc_p": 70, "degree_p": 70,
        "etest_p": 70, "mba_p": 65,
        "gender": "M", "ssc_b": "Central", "hsc_b": "Central",
        "hsc_s": hsc_s, "degree_t": degree_t,
        "workex": workex, "specialisation": specialisation
    }])

    for col in place_cat_cols:
        try:
            inp[col] = place_encoders[col].transform(inp[col].astype(str))
        except ValueError:
            inp[col] = 0

    prob = place_pipeline.predict_proba(inp)[0][1]
    return round(float(prob) * 100, 2)

def detect_skill_gaps(resume_text, primary_role):
    """
    ML-based skill gap detection:
    Compare skills found in resume vs required skills for the role
    using the job_roles.json data built from LinkedIn dataset
    """
    resume_lower = resume_text.lower()

    SKILL_KEYWORDS = {
        "Python":           ["python"],
        "Java":             ["java"],
        "JavaScript":       ["javascript", "js"],
        "SQL":              ["sql", "mysql", "postgresql", "database"],
        "Machine Learning": ["machine learning", "ml", "sklearn", "scikit"],
        "Deep Learning":    ["deep learning", "tensorflow", "pytorch", "keras"],
        "NLP":              ["nlp", "natural language", "bert", "transformers"],
        "Docker":           ["docker", "containerization"],
        "Kubernetes":       ["kubernetes", "k8s"],
        "AWS":              ["aws", "amazon web services", "ec2", "s3"],
        "Azure":            ["azure", "microsoft cloud"],
        "GCP":              ["gcp", "google cloud"],
        "React":            ["react", "reactjs"],
        "Node.js":          ["node", "nodejs", "express"],
        "Git":              ["git", "github", "version control"],
        "Linux":            ["linux", "unix", "bash"],
        "Data Analysis":    ["data analysis", "pandas", "numpy", "matplotlib"],
        "Computer Vision":  ["computer vision", "opencv", "image processing"],
        "Statistics":       ["statistics", "probability", "regression"],
        "Communication":    ["communication", "presentation", "teamwork"],
        "Leadership":       ["leadership", "team lead", "managed", "mentored"],
        "Agile":            ["agile", "scrum", "sprint", "jira"],
        "C++":              ["c++", "cpp"],
        "System Design":    ["system design", "architecture", "distributed systems"],
        "Cloud Computing":  ["cloud", "cloud computing", "saas", "paas"],
        "DevOps":           ["devops", "ci/cd", "jenkins", "pipeline"],
        "Cybersecurity":    ["security", "cybersecurity", "penetration", "firewall"],
        "REST API":         ["rest", "api", "fastapi", "flask", "django"],
        "TypeScript":       ["typescript", "ts"],
        "Flutter":          ["flutter", "dart"],
        "Android":          ["android", "kotlin"],
        "iOS":              ["ios", "swift", "xcode"],
    }

    # Detect skills present in resume
    skills_present = [
        skill for skill, keywords in SKILL_KEYWORDS.items()
        if any(kw in resume_lower for kw in keywords)
    ]

    # Role-specific commonly required skills
    role_common_skills = {
        "Machine Learning Engineer": ["NLP", "Cloud Computing", "System Design", "Docker", "Kubernetes"],
        "Data Scientist":            ["Statistics", "Deep Learning", "Cloud Computing", "Communication"],
        "Software Engineer":         ["System Design", "Agile", "Docker", "REST API", "Linux"],
        "Frontend Developer":        ["TypeScript", "React", "Git", "REST API", "Communication"],
        "Backend Developer":         ["Docker", "System Design", "SQL", "REST API", "Linux"],
        "Full Stack Developer":      ["Docker", "System Design", "TypeScript", "Agile"],
        "DevOps Engineer":           ["Kubernetes", "AWS", "Linux", "Docker", "System Design"],
        "Data Analyst":              ["Statistics", "SQL", "Communication", "Data Analysis", "Python"],
        "Data Engineer":             ["AWS", "Docker", "SQL", "Python", "System Design"],
        "Cloud Engineer":            ["AWS", "Docker", "Kubernetes", "Linux", "System Design"],
        "Cybersecurity Analyst":     ["Linux", "Python", "Cybersecurity", "Communication"],
        "Mobile Developer":          ["Flutter", "Android", "iOS", "REST API", "Git"],
        "QA Engineer":               ["Agile", "Python", "REST API", "Communication", "Git"],
        "Product Manager":           ["Agile", "Communication", "Leadership", "Statistics"],
        "Project Manager":           ["Agile", "Leadership", "Communication"],
        "UI/UX Designer":            ["Communication", "Agile", "Leadership"],
        "Database Administrator":    ["SQL", "Linux", "Python", "System Design"],
        "Network Engineer":          ["Linux", "Cybersecurity", "System Design", "Communication"],
        "Marketing Manager":         ["Communication", "Leadership", "Statistics", "Data Analysis"],
    }

    # Find missing skills for the role
    skills_missing = [
        s for s in role_common_skills.get(primary_role, [])
        if s not in skills_present
    ][:5]

    return skills_present, skills_missing

def get_groq_advice(resume_text, primary_role, ranked_roles):
    roles_str = ", ".join([r["role"] for r in ranked_roles])

    prompt = f"""
You are a career advisor AI. Analyze this resume and provide structured advice.

RESUME:
{resume_text[:3000]}

PRIMARY ROLE MATCH: {primary_role}
OTHER SUITABLE ROLES: {roles_str}

Respond with valid JSON only, no extra text, no markdown:
{{
  "weak_areas": ["2-3 weak areas that need improvement based on the resume"],
  "how_to_bridge": ["3-5 actionable steps to improve chances for {primary_role}"],
  "suitable_roles": ["top 3 roles from the list that best fit this resume"],
  "career_advice": "2-3 sentence personalized career advice"
}}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "weak_areas":     [],
            "how_to_bridge":  [],
            "suitable_roles": [primary_role],
            "career_advice":  raw
        }

# ── Routes ────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "ResumeIQ API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/roles")
def get_roles():
    return {"roles": list(job_roles.keys())}

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    # Validate
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    # Extract text
    resume_text = extract_pdf_text(file_bytes)
    if len(resume_text) < 50:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    # ML predictions
    job_match        = match_jobs(resume_text)
    placement_chance = predict_placement(resume_text)

    # ML-based skill gap detection
    skills_present, skills_missing = detect_skill_gaps(
        resume_text,
        job_match["primary_role"]
    )

    # Groq advice (weak areas, how to bridge, career advice only)
    advice = get_groq_advice(
        resume_text,
        job_match["primary_role"],
        job_match["ranked_roles"]
    )

    # Role metadata
    role_info = job_roles.get(job_match["primary_role"], {})

    return {
        "primary_role":     job_match["primary_role"],
        "rf_confidence":    job_match["rf_confidence"],
        "ranked_roles":     job_match["ranked_roles"],
        "placement_chance": placement_chance,
        "required_skills":  skills_present,                    # ← ML detected
        "avg_salary":       role_info.get("avg_salary"),
        "skills_found":     skills_present,                    # ← ML detected
        "gap_analysis": {
            "missing_skills": skills_missing,                  # ← ML detected
            "weak_areas":     advice.get("weak_areas", [])    # ← Groq
        },
        "how_to_bridge":    advice.get("how_to_bridge", []),   # ← Groq
        "suitable_roles":   advice.get("suitable_roles", []),  # ← Groq
        "career_advice":    advice.get("career_advice", ""),   # ← Groq
    }