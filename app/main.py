import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_connection
from app.services.serve import get_companies, get_reviews_by_company, get_insights_by_company

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def list_companies():
    companies = get_companies()
    return {"companies": companies}

@app.get("/companies/{company_id}/reviews")
async def list_reviews(company_id: int):
    reviews = get_reviews_by_company(company_id)
    return {"reviews": reviews}

@app.get("/companies/{company_id}/insights")
async def list_insights(company_id: int):
    insights = get_insights_by_company(company_id)
    return {"insights": insights}

