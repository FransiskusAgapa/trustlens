from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the TrustLens API"}

def test_health_():
    response = client.get('/health')
    assert response.status_code == 200
    assert "status" in response.json()

def test_companies_endpoint():
    with patch("app.main.get_companies", return_value=[{"id": 1, "name": "ALDI"}]):
        response = client.get('/companies')
    assert response.status_code == 200
    assert "companies" in response.json()

def test_reviews_endpoint():
    with patch("app.main.get_reviews_by_company", return_value=[]):
        response = client.get('/companies/1/reviews')
    assert response.status_code == 200
    assert "reviews" in response.json()

def test_insights_endpoint():
    with patch("app.main.get_insights_by_company", return_value=[]):
        response = client.get('/companies/1/insights')
    assert response.status_code == 200
    assert "insights" in response.json()

def test_rate_limit_exceeded():
    with patch("app.main.rate_limiter.is_allowed", return_value=False):
        response = client.get('/companies')
    assert response.status_code == 429


