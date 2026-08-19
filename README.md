# TrustLens

TrustLens is a Glassdoor review intelligence dashboard that ingests real employee reviews, runs AI-powered sentiment and department analysis, and surfaces actionable insights for HR teams and startup founders. A Head of Talent can identify which departments are driving negative sentiment across multiple companies in under 30 seconds.

## Live Demo

- Frontend: https://trustlens-frontend-59k1.onrender.com
- Backend API: https://trustlens-api-bywi.onrender.com
- AI-DLC Documentation: [AI_DEVELOPMENT.md](./AI_DEVELOPMENT.md)

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Axios, Recharts |
| Backend | Python, FastAPI, uvicorn |
| Database | PostgreSQL |
| AI | Azure OpenAI (GPT-35-turbo) |
| CI/CD | GitHub Actions |
| Hosting | Render |
| Testing | pytest, unittest.mock |

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/FransiskusAgapa/trustlens.git
cd trustlens
```

### 2. Create your environment file

```bash
cp .env.example .env
```

Fill in your values:
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/trustlens
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT=your_deployment_name


### 3. Set up the database

```bash
psql -U postgres -c "CREATE DATABASE trustlens;"
psql -U postgres -d trustlens -f db/schema.sql
```

### 4. Install backend dependencies and seed data

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python seed.py
```

### 5. Run the backend

```bash
uvicorn app.main:app --reload
```

API runs at: http://localhost:8000

### 6. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

## Project Structure
trustlens/
├── app/
│ ├── main.py # FastAPI app, routes, CORS, rate limiter
│ ├── database.py # PostgreSQL connection
│ ├── rate_limiter.py # Token bucket rate limiter
│ └── services/
│ ├── analyze.py # Azure OpenAI integration
│ ├── processor.py # ReviewProcessor class (batch AI analysis)
│ ├── insight_engine.py # InsightEngine class (heap-based ranking)
│ └── serve.py # Database query functions
├── db/
│ └── schema.sql # Idempotent database schema
├── frontend/
│ └── src/
│ ├── App.jsx # Main app with navigation
│ ├── api.js # Central axios instance
│ └── components/
│ ├── CompanyList.jsx
│ ├── ReviewFeed.jsx
│ ├── InsightsPanel.jsx
│ └── ComparisonView.jsx
├── scripts/ # One-time scripts (not discoverable by pytest)
│ ├── run_processor.py
│ └── run_insight_engine.py
├── tests/ # Unit tests
│ ├── test_processor.py
│ └── test_insight_engine.py
├── seed.py # Seed database from Glassdoor CSV
├── AI_DEVELOPMENT.md # AI-DLC methodology documentation
└── requirements.txt


## Running Tests

```bash
pytest tests/ -v
```

## Built With AI-DLC

This project was built using an AI-driven development lifecycle where Claude guided every architectural decision. See [AI_DEVELOPMENT.md](./AI_DEVELOPMENT.md) for the full methodology documentation.