from unittest.mock import MagicMock, patch

from app.services.serve import get_companies, get_reviews_by_company, get_insights_by_company

def make_mock_conn(rows, columns):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchall.return_value = rows
    mock_cur.description = [(col,) for col in columns]
    return mock_conn

def test_get_companies():
    mock_conn = make_mock_conn(
        rows=[(1, "ALDI", "Retail", "Large", "2024-01-01")],
        columns=["id", "name", "industry", "size", "created_at"]
    )
    with patch("app.services.serve.get_connection", return_value=mock_conn):
        result = get_companies()
    assert len(result) == 1
    assert result[0]["name"] == "ALDI"

def test_get_reviews_by_company():
    mock_conn = make_mock_conn(
        rows=[(1, 1, None, "Great culture", 5, "2024-01-01")],
        columns=["id", "company_id", "department_id", "content", "rating", "created_at"]
    )
    with patch("app.services.serve.get_connection", return_value=mock_conn):
        result = get_reviews_by_company(1)
    assert len(result) == 1
    assert result[0]["content"] == "Great culture"

def test_get_insights_by_company():
    mock_conn = make_mock_conn(
        rows=[(1, 1, "positive", 0.9, ["culture"], "management", "Great place", "2024-01-01", "2024-01-01")],
        columns=["id", "review_id", "sentiment_label", "sentiment_score", "themes", "department_tag", "summary", "processed_at", "review_date"]
    )
    with patch("app.services.serve.get_connection", return_value=mock_conn):
        result = get_insights_by_company(1)
    assert len(result) == 1
    assert result[0]["sentiment_label"] == "positive"