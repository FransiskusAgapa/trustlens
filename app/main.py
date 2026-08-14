import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_connection
from app.services.serve import get_companies, get_reviews_by_company, get_insights_by_company
from app.rate_limiter import TokenBucket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rate_limiter = TokenBucket(capacity=10, refill_rate=1) 


@app.get("/")
async def root():
    return {"message": "Hey, Welcome to the TrustLens API!"}

@app.get("/health")
async def health():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/companies")
async def list_companies(request: Request):
    if not rate_limiter.is_allowed(request.client.host):
        raise HTTPException(status_code=429, detail="Too Many Requests")
    return {"companies": get_companies()}

@app.get("/companies/{company_id}/reviews")
async def list_reviews(company_id: int):
    return {"reviews": get_reviews_by_company(company_id)}

@app.get("/companies/{company_id}/insights")
async def list_insights(company_id: int):
    return {"insights": get_insights_by_company(company_id)}
