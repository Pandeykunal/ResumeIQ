# 🎯 ResumeIQ — AI-Powered Resume Analyzer & Career Advisor

ResumeIQ is a full-stack AI application that analyzes your resume and predicts the best-fit job roles using a trained Random Forest classifier, ranks all suitable roles via TF-IDF cosine similarity, predicts placement probability using Logistic Regression, detects skill gaps through an ML pipeline, and generates personalized career advice using Groq's Llama 3.3 LLM.

---

## 📸 Demo

📹 **[Watch Demo Video & Screenshots](https://drive.google.com/drive/folders/1uRge6QweVzTFi4lPd63EP9zd4ZC-m-6S?usp=sharing)**

---

## 📂 Datasets

📁 **[Download Datasets](https://drive.google.com/drive/folders/1vS77_uku0VVUoEYt9zuLrbKXT33m_9I9?usp=sharing)**

| Dataset | Source | Size | Used For |
|---|---|---|---|
| LinkedIn Job Postings | Kaggle | 123,849 jobs | Job role classification + cosine similarity |
| Campus Placement | Kaggle | 215 records | Placement % prediction |

---

## ✨ Features

| Feature | Description | Powered By |
|---|---|---|
| 🎯 **Primary Role Prediction** | Predicts best job role from resume | Random Forest (87.91% accuracy) |
| 📊 **Role Confidence Score** | Confidence % of role prediction | Random Forest |
| 📐 **Role Similarity Ranking** | Ranks all 19 roles by resume fit | TF-IDF Cosine Similarity |
| 📈 **Placement Chance %** | Probability of getting placed | Logistic Regression (83.72% accuracy) |
| 💰 **Salary Insights** | Average salary for predicted role | LinkedIn Dataset (123K+ jobs) |
| 🔍 **Skills Detection** | Detects skills present in resume | ML Rule-based NLP Pipeline |
| ❌ **Missing Skills** | Identifies skill gaps for target role | ML Role-Skill Mapping |
| ⚠️ **Weak Areas** | Areas needing improvement | Groq Llama 3.3 70B |
| 🚀 **How to Bridge** | Actionable steps to improve | Groq Llama 3.3 70B |
| 💡 **Career Advice** | Personalized career guidance | Groq Llama 3.3 70B |

---

## 🏗️ Architecture

```
User uploads Resume PDF
         │
         ▼
   React Frontend
   (Vite + Tailwind)
         │
         ▼ HTTP POST /analyze
   FastAPI Backend
         │
    ┌────┴─────────────────────────────────┐
    │                                      │
    ▼                                      ▼
pdfplumber                         ML Pipeline
extracts text                           │
    │                      ┌────────────┼────────────┐
    └──────────────────────►            │            │
                           ▼            ▼            ▼
                     TF-IDF       Random       Cosine
                     Vectorizer   Forest       Similarity
                           │            │            │
                           └────────────┼────────────┘
                                        │
                           ┌────────────┼────────────┐
                           ▼            ▼            ▼
                      Logistic    Skill Gap      Groq AI
                     Regression   Detection    (Llama 3.3)
                      (Place %)   (ML-based)   (Advice)
                           │            │            │
                           └────────────┼────────────┘
                                        │
                                        ▼
                                  JSON Response
                                        │
                                        ▼
                               React Result Page
```

---

## 🛠️ Tech Stack

### Machine Learning
- **Random Forest Classifier** — Job role prediction (19 classes, 87.91% accuracy)
- **TF-IDF Vectorizer** — Text to numerical features (8000 features, bigrams)
- **Cosine Similarity** — Role ranking against 19 role centroids
- **Logistic Regression** — Placement probability prediction (83.72% accuracy, ROC-AUC: 0.93)
- **Rule-based NLP** — Skill extraction and gap detection

### Datasets
- **LinkedIn Job Postings** — 123,849 job postings across 19 role categories
- **Campus Placement Dataset** — 215 student records for placement prediction

### Backend
- **FastAPI** — REST API framework
- **pdfplumber** — PDF text extraction
- **scikit-learn** — ML model inference
- **Groq API (Llama 3.3 70B)** — Natural language advice generation

### Frontend
- **React 18** — UI framework
- **Vite** — Build tool
- **Tailwind CSS** — Styling
- **React Router** — Navigation
- **Axios** — API calls

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/Pandeykunal/ResumeIQ.git
cd ResumeIQ/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_key_here > .env

# Add model files to backend/models/ and data/ folder
# (Train using notebooks/AI_Resume_Checker_Training_V2.ipynb)

# Run backend
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 🤖 How It Works

### Step 1 — Training Phase (Google Colab)
```
LinkedIn Dataset (123K jobs)
        ↓
Label 19 job role categories
        ↓
TF-IDF vectorize job descriptions
        ↓
Train Random Forest (200 trees) → 87.91% accuracy
Build Cosine Similarity centroids → 19 role vectors
        ↓
Campus Placement Dataset (215 records)
        ↓
Train Logistic Regression → 83.72% accuracy, ROC-AUC: 0.93
        ↓
Export .pkl files
```

### Step 2 — Inference Phase (FastAPI)
```
PDF Resume uploaded
        ↓
pdfplumber extracts text
        ↓
TF-IDF vectorizes resume text
        ↓
Random Forest → Primary Role + Confidence %
Cosine Similarity → All 19 roles ranked
Logistic Regression → Placement %
Rule-based NLP → Skills found + Missing skills
Groq Llama 3.3 → Weak areas + How to bridge + Career advice
        ↓
JSON response → React displays results
```

---

## 📊 Model Performance

| Model | Accuracy | Notes |
|---|---|---|
| Random Forest (Job Role) | **87.91%** | 19 classes, 9,500+ training samples |
| Logistic Regression (Placement) | **83.72%** | ROC-AUC: 0.93 |
| TF-IDF Cosine Similarity | — | Ranking metric, not classification |

---

## 🎓 What I Learned

- End-to-end ML pipeline from data collection to production
- Multi-class text classification using Random Forest + TF-IDF
- Cosine similarity for document ranking
- Logistic Regression for binary probability prediction
- FastAPI for serving ML models as REST APIs
- React + Tailwind for building modern UIs
- LLM integration (Groq) for natural language generation
- Combining traditional ML with LLMs in one system

---

## 🗺️ Future Improvements

- [ ] Add BERT-based resume parsing for better skill extraction
- [ ] Support DOCX resume format
- [ ] Add desired job role input for targeted gap analysis
- [ ] Deploy on cloud with model compression
- [ ] Add resume scoring out of 100
- [ ] Multi-language resume support

---


Made with ❤️ by Kunal Pandey

</div>
