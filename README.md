# Fake News Detection System

> A web application that detects fake news using DeBERTa-v3, RAG pipeline, and 7 verdict categories.

**Status:** 🚧 In Progress — Phase 1 (Steps 1-5 of 19 complete)

---

## What This Project Does

A user pastes a news article URL or text into a web app. The system analyzes it and returns one of 7 verdicts — REAL, FAKE, MISLEADING, SATIRE, UNVERIFIED, IMPLAUSIBLE, or STALE — along with a confidence score, reasoning, and links to verified sources that support the verdict.

What makes this different from other fake news detectors:

- **7 verdict categories** instead of binary real/fake — more honest about uncertainty
- **Plausibility layer** that catches impossible claims before the ML model even runs
- **RAG pipeline** that gives the LLM real verified sources to cite instead of hallucinating
- **Satire detection** so parody sites are never mislabeled as misinformation

---

## Architecture Overview

```
User (Browser)
      |
      v
React Frontend (Vercel)
      |
      v
FastAPI Backend (Railway)
      |
      |-----> Plausibility Check (spaCy + Groq)
      |-----> DeBERTa-v3 Classifier
      |-----> Qdrant Vector Search
      |-----> NewsAPI Real-time Search
      |-----> Groq LLM (Llama 3.1) RAG Pipeline
      |
      v
JSON Response → Frontend renders verdict card

Background (every 30 min):
Ingestion Pipeline → RSS Feeds + Google Fact Check + Wikipedia → Qdrant
```

---

## The 7 Verdict Categories

| Verdict     | When Assigned                          | Example                                            |
| ----------- | -------------------------------------- | -------------------------------------------------- |
| REAL        | Supported by multiple verified sources | Reuters article confirmed by 3 sources             |
| FAKE        | Directly contradicted by evidence      | Health claim debunked by WHO                       |
| MISLEADING  | True facts but deceptively framed      | 10-year-old stat presented as current              |
| SATIRE      | Source is a known parody site          | Any article from theonion.com                      |
| UNVERIFIED  | Too new — no matching sources yet      | Breaking news from last hour                       |
| IMPLAUSIBLE | Defies physical or factual reality     | Aliens landing, dead politicians winning elections |
| STALE       | Article is more than 2 years old       | 2012 article recirculating as current news         |

---

## Tech Stack

### Backend

| Tool                  | Purpose                                           |
| --------------------- | ------------------------------------------------- |
| Python + FastAPI      | Web API framework                                 |
| DeBERTa-v3-base       | Core fake news classifier (fine-tuned on WELFake) |
| Qdrant                | Vector database storing verified news embeddings  |
| sentence-transformers | Converts text to vectors for Qdrant               |
| Groq API (Llama 3.1)  | LLM for RAG pipeline verdicts                     |
| spaCy                 | Named entity recognition for plausibility layer   |
| feedparser            | RSS feed parser for ingestion pipeline            |
| APScheduler           | Runs ingestion job every 30 minutes               |
| readability-lxml      | Extracts clean article text from URLs             |
| python-dotenv         | Manages API keys via .env file                    |

### Frontend

| Tool            | Purpose                         |
| --------------- | ------------------------------- |
| React 18 + Vite | UI framework                    |
| Tailwind CSS    | Styling                         |
| axios           | HTTP client for calling backend |

### External Services

| Service               | Purpose                              | Cost           |
| --------------------- | ------------------------------------ | -------------- |
| Qdrant Cloud          | Vector database hosting              | Free tier      |
| Groq API              | LLM inference (6000 req/day)         | Free           |
| Google Fact Check API | Pre-labeled verdicts from Snopes etc | Free           |
| NewsAPI               | Real-time news search                | Free (100/day) |
| Vercel                | Frontend hosting                     | Free           |
| Railway               | Backend hosting                      | Free tier      |

---

## Project Structure

```
fake-news-detector/
  ml-service/                  ← Python backend
    main.py                    ← FastAPI app entry point
    pipeline.py                ← Main analysis pipeline
    classifier.py              ← DeBERTa-v3 inference
    plausibility.py            ← Plausibility layer
    credibility.py             ← Domain credibility scorer
    extractor.py               ← URL article extraction
    rag.py                     ← RAG pipeline + LLM call
    ingest/
      ingest.py                ← Main ingestion runner
      rss_parser.py            ← RSS feed parser
      fact_check.py            ← Google Fact Check API
      wikipedia_ingest.py      ← Wikipedia API
    requirements.txt
    .env                       ← API keys (never commit)

  frontend/                    ← React app
    src/
      App.jsx
      components/
        InputForm.jsx
        VerdictCard.jsx
        SourceList.jsx

  notebooks/
    eda.ipynb                  ← Dataset exploration (✅ complete)
    training.ipynb             ← DeBERTa fine-tuning (🚧 pending)

  docs/
    test_results.md            ← (🚧 pending — Step 12)
    demo_cases.md              ← (🚧 pending — Step 17)

  README.md
  .gitignore
```

---

## Dataset Analysis (Step 2 — ✅ Complete)

### WELFake Dataset

- **Total articles:** 72,134
- **Real (label=1):** 37,106
- **Fake (label=0):** 35,028
- **Balance:** Nearly equal — no major class imbalance
- **Average title length:** 12.27 words
- **Average body length:** 540.84 words
- **Missing titles:** 558 (will be handled during training)
- **Source:** Kaggle — saurabhshahane/fake-news-classification

### LIAR Dataset

- **Total statements:** 12,836
- **Train / Test / Val split:** 10,269 / 1,283 / 1,284
- **Labels:** 6 categories (mapped to binary for cross-dataset testing)
- **Source:** William Yang Wang, ACL 2017

#### LIAR Label Distribution

| Label       | Count |
| ----------- | ----- |
| half-true   | 2,123 |
| False       | 1,998 |
| mostly-true | 1,966 |
| True        | 1,683 |
| barely-true | 1,657 |
| pants-fire  | 842   |

#### Binary Mapping for Cross-Dataset Testing

- **REAL (1):** true, mostly-true, half-true
- **FAKE (0):** false, barely-true, pants-fire

---

## Accuracy Targets

| Model                        | Dataset            | Target F1 |
| ---------------------------- | ------------------ | --------- |
| Logistic Regression baseline | WELFake test split | 70-75%    |
| DeBERTa-v3                   | WELFake test split | 90%+      |
| DeBERTa-v3 cross-dataset     | LIAR test split    | 80%+      |

---

## ML Results

> 🚧 This section will be updated after Step 3 (Logistic Regression) and Step 6 (DeBERTa training)

| Model               | WELFake F1 | LIAR F1 |
| ------------------- | ---------- | ------- |
| Logistic Regression | TBD        | —       |
| DeBERTa-v3          | TBD        | TBD     |

---

## Local Setup

> 🚧 Full setup instructions will be added after all components are built (Step 18)

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop
- Git

### Quick Start (Backend)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/fake-news-detector.git
cd fake-news-detector/ml-service

# 2. Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
source venv/bin/activate        # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add API keys to .env
cp .env.example .env
# Fill in your keys

# 5. Start Qdrant locally
docker run -p 6333:6333 qdrant/qdrant

# 6. Run the backend
uvicorn main:app --reload --port 8000
```

---

## Environment Variables

```bash
# ml-service/.env — never commit this file
GROQ_API_KEY=           # console.groq.com
GOOGLE_FACTCHECK_API_KEY=  # console.cloud.google.com
NEWSAPI_KEY=            # newsapi.org
QDRANT_URL=             # cloud.qdrant.io
QDRANT_API_KEY=         # cloud.qdrant.io
```

---

## API Endpoints

> 🚧 Full API documentation will be added after Step 7

### POST /analyze

Analyzes a news article and returns a verdict.

**Request:**

```json
{
  "text": "article body text",
  "source_url": "https://example.com/article",
  "article_date": "2024-03-15"
}
```

**Response:**

```json
{
  "verdict": "REAL | FAKE | MISLEADING | SATIRE | UNVERIFIED | IMPLAUSIBLE | STALE",
  "confidence": 0.92,
  "credibility_score": 0.99,
  "domain": "reuters.com",
  "article_date": "2024-03-15",
  "stale_warning": false,
  "reasoning": "Article confirmed by 3 independent sources...",
  "flagged_sentences": ["suspicious sentence 1"],
  "fact_checks": [{ "title": "...", "url": "...", "org": "Snopes" }],
  "related_articles": [{ "title": "...", "url": "...", "source": "Reuters" }]
}
```

---

## Progress Tracker

### Phase 1 — ML Foundation (Weeks 1-3)

| Step   | Description                         | Status      |
| ------ | ----------------------------------- | ----------- |
| Step 1 | Project Setup & Environment         | ✅ Complete |
| Step 2 | Download Datasets & EDA             | ✅ Complete |
| Step 3 | Train Logistic Regression Baseline  | ✅ Complete |
| Step 4 | Build Domain Credibility Scorer     | ✅ Complete |
| Step 5 | Build RSS Parser & Ingestion Script | ✅ Complete |
| Step 6 | Fine-tune DeBERTa-v3                | ⏳ Pending  |
| Step 7 | Expose /predict Endpoint            | ⏳ Pending  |

### Phase 2 — Plausibility Layer + RAG (Weeks 4-5)

| Step    | Description                     | Status     |
| ------- | ------------------------------- | ---------- |
| Step 8  | Build Plausibility Layer        | ⏳ Pending |
| Step 9  | Build RAG Pipeline              | ⏳ Pending |
| Step 10 | Build URL Article Extractor     | ⏳ Pending |
| Step 11 | Wire Full Pipeline with Routing | ⏳ Pending |
| Step 12 | End-to-End Testing 20 Articles  | ⏳ Pending |

### Phase 3 — Frontend + Deploy (Week 6)

| Step    | Description               | Status     |
| ------- | ------------------------- | ---------- |
| Step 13 | Add Scheduled Ingestion   | ⏳ Pending |
| Step 14 | Build React Frontend      | ⏳ Pending |
| Step 15 | Deploy Backend to Railway | ⏳ Pending |
| Step 16 | Deploy Frontend to Vercel | ⏳ Pending |

### Phase 4 — Polish & Submit (Week 7)

| Step    | Description                 | Status     |
| ------- | --------------------------- | ---------- |
| Step 17 | Prepare 5 Demo Cases        | ⏳ Pending |
| Step 18 | Write Complete README       | ⏳ Pending |
| Step 19 | Code Cleanup & Final Checks | ⏳ Pending |

---

## Known Limitations

> 🚧 Will be expanded as the project develops

- Paywalled articles require manual text pasting
- Non-English articles not supported
- Breaking news (under 1 hour old) may return UNVERIFIED due to lack of sources

---

## Future Improvements

- Multilingual support
- User feedback loop to improve verdicts over time
- Image and video fake news detection
- Browser extension for one-click checking

---

## License

For educational and research purposes only.

---

_Last updated: Step 5 complete — RSS Parser & Ingestion Pipeline built and tested (109 vectors stored in Qdrant)_
