import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_connection
from app.services.serve import get_companies, get_reviews_by_company, get_insights_by_company
from app.rate_limiter import TokenBucket

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://trustlens-frontend-59k1.onrender.com",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rate_limiter = TokenBucket(capacity=10, refill_rate=1)

def check_rate_limit(request: Request):
    if not rate_limiter.is_allowed(request):
        logger.warning("Rate limit exceeded for request")
        raise HTTPException(status_code=429, detail="Too many requests. Please slow down.")

@app.get("/")
def root():
    return {"message": "Welcome to the TrustLens API"}

@app.get("/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "healthy"}
    except Exception as e:
        logger.error("Health check failed: %s", e)
        return {"status": "unhealthy"}

@app.get("/companies")
def list_companies(request: Request):
    check_rate_limit(request)
    return {"companies": get_companies()}

@app.get("/companies/{company_id}/reviews")
def list_reviews(request: Request, company_id: int):
    check_rate_limit(request)
    return {"reviews": get_reviews_by_company(company_id)}

@app.get("/companies/{company_id}/insights")
def list_insights(request: Request, company_id: int):
    check_rate_limit(request)
    return {"insights": get_insights_by_company(company_id)}