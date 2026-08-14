# AI-Driven Development: TrustLens

## Project Overview

TrustLens is a Glassdoor review intelligence dashboard that ingests real employee 
reviews, runs AI-powered sentiment and department analysis, and surfaces actionable 
insights for HR teams and startup founders. Built in 28 days using the same AI-DLC 
methodology as ReviewSense, TrustLens is the repeatability proof that the process 
works across different business domains.

---

## Business Outcome

**Problem:**
Glassdoor shows individual reviews but provides no way to filter sentiment by 
department, compare sentiment across companies, or identify which specific areas 
of a company are driving employee dissatisfaction. Manual analysis of hundreds of 
reviews takes hours with no guarantee of consistency.

**Solution:**
TrustLens ingests real Glassdoor reviews, runs Azure OpenAI analysis extracting 
sentiment label, confidence score, themes, department tag, and a one-line summary 
per review, and surfaces ranked insights grouped by department. A comparison view 
lets users benchmark two companies side by side.

**Value delivered:**
A Head of Talent can identify which departments are driving negative employee 
sentiment across multiple companies in under 30 seconds, replacing hours of manual 
Glassdoor review reading with no ability to filter by department or compare 
companies side by side.

**Cost without AI-DLC:**
3-4 months for a small team of 2-3 engineers with separate frontend, backend, 
data engineering, and AI integration specialists.

**Cost with AI-DLC:**
28 days, one developer, using Claude as architectural guide at every layer.

**Repeatability proof:**
TrustLens is Project 2 in a 10-project AI-DLC ladder. ReviewSense (Project 1) 
solved Amazon review intelligence in 28 days. TrustLens solved Glassdoor review 
intelligence in 28 days using the identical methodology. Different domain, same 
process, same production quality outcome. This is the definition of a repeatable 
process.

---

## What is AI-DLC?

AI-DLC means using AI at every stage of the software development lifecycle. Not 
just for code generation. For architectural decisions, concept explanation, 
debugging strategy, testing design, and deployment planning.

TrustLens is proof of that process applied twice.

---

## Architecture Decisions Guided by AI

### Schema Design
4-table normalized PostgreSQL schema with a global departments lookup table 
(not company-specific), nullable department_id on reviews to handle anonymous 
Glassdoor data, and JSONB for AI theme storage. The decision to make department_id 
nullable came from recognizing that Glassdoor reviews don't include department 
information and fabricating it would corrupt the data.

**Business reason:** Data integrity at the schema level prevents bad data from 
entering the system regardless of what the application layer does.

### Richer AI Output
TrustLens prompts Azure OpenAI for 5 fields instead of ReviewSense's 3: 
sentiment_label, sentiment_score, themes, department_tag, and summary. The 
department_tag lets the AI infer which business area a review addresses even when 
the reviewer didn't specify one.

**Business reason:** Department-level insights are what make TrustLens actionable 
for HR teams. Generic sentiment without department context is not enough to drive 
decisions.

### Department-Grouped InsightEngine
InsightEngine groups themes by department_tag using a dictionary of Counters before 
applying heapq.nlargest. This gives ranked themes per department instead of globally.

**Business reason:** A Head of Talent asking "what are people saying about our 
compensation?" needs department-filtered insights, not a flat list of all themes.

### Comparison View
A fourth React view allows users to select two companies and see their sentiment 
distributions side by side. This required passing the full company object through 
props (not just the ID) so the company name was available in child components.

**Business reason:** Benchmarking against competitors is a core use case for HR 
teams making hiring pitches and talent strategy decisions.

### Per-Company Processor
The ReviewProcessor was extended to accept a company_id parameter, allowing 
controlled processing of exactly 20 reviews per company for cost management.

**Business reason:** Azure OpenAI costs money per token. Processing 5,000 reviews 
when 20 per company is enough for demonstration wastes budget. Production systems 
must be cost-aware.

### Token Bucket Rate Limiter
Same token bucket algorithm as ReviewSense. 10 tokens per IP, 1 token refill per 
second, HTTP 429 on empty bucket.

**Business reason:** Protects the API from abuse and controls Azure OpenAI costs 
at the infrastructure level, not just the application level.

---

## What I Built vs What Claude Guided

| Layer | Claude Guided | I Built |
|---|---|---|
| Database | 4-table schema, nullable department_id decision, JSONB | All 4 CREATE TABLE statements from memory |
| Backend | FastAPI routing, serve.py patterns, response shape consistency | All endpoints, service modules, consistent {"key": [...]} response format |
| AI Integration | 5-field prompt design, department_tag inference concept | analyze.py with richer prompt, processor with company_id filter |
| Algorithms | Department-grouped heap ranking concept | InsightEngine with Counter dictionary grouped by department_tag |
| Rate Limiting | Token bucket per-IP tracking pattern | Full TokenBucket class with clients dictionary |
| Testing | Mock patterns, AAA, fixture design | 3 unit tests all passing in CI |
| CI/CD | GitHub Actions syntax, main vs master branch standard | ci.yml pipeline, branch rename to main |
| Frontend | 4-view architecture, comparison view state design | All 4 React components including ComparisonView with dropdown |
| Deployment | Render deployment pattern, per-company seeding strategy | Full deployment, seed_insights.py for controlled processing |

---

## Key Technical Learnings

- **Nullable vs NOT NULL is a data integrity decision:** Making department_id 
  nullable was not laziness. It was honest data modeling. We don't know the 
  department from Glassdoor data so we don't fabricate it.
- **API response shape consistency matters:** Inconsistent response shapes 
  (sometimes array, sometimes nested object) caused real debugging time. Enforcing 
  {"key": [...]} everywhere eliminated that class of bug.
- **Per-client rate limiting requires per-client state:** A global token counter 
  doesn't protect against one client abusing the API. Each IP needs its own bucket.
- **Cost awareness is a production concern from day one:** Processing 100 reviews 
  instead of 5,000 is an engineering decision, not a shortcut. Production systems 
  must manage costs explicitly.
- **Repetition reveals what you actually know:** Building TrustLens after 
  ReviewSense exposed exactly which concepts were understood deeply and which were 
  just memorized. The gaps showed up immediately and were filled properly this time.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Axios |
| Backend | Python, FastAPI, uvicorn |
| Database | PostgreSQL |
| AI | Azure OpenAI (GPT-35-turbo) |
| CI/CD | GitHub Actions |
| Hosting | Render |
| Testing | pytest, unittest.mock |

---

## Live URLs

- Frontend: https://trustlens-frontend-ajub.onrender.com
- Backend: https://trustlens-api-bywi.onrender.com
- GitHub: https://github.com/FransiskusAgapa/trustlens
- ReviewSense (Project 1): https://reviewsense-frontend-p2qj.onrender.com