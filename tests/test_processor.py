import pytest
from unittest.mock import MagicMock, patch

from app.services.processor import ReviewProcessor

def test_fetch_unprocessed_reviews():
    # arrange
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "This is a great product!"),]

    with patch("app.services.processor.get_connection", return_value=mock_conn):
        processor = ReviewProcessor()
        processor.conn = mock_conn
        processor.cur = mock_cursor

        # act
        reviews = processor.fetch_unprocessed_reviews()

        # assert 
        assert reviews == [
            (1, "This is a great product!")
        ]

def test_save_processed_review():
    # arrange
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("app.services.processor.get_connection", return_value=mock_conn):
        processor = ReviewProcessor()
        processor.conn = mock_conn
        processor.cur = mock_cursor

        fake_result = '{"sentiment_label": "positive", "sentiment_score": 0.9, "themes": ["culture", "management", "compensation"], "department_tag": "culture", "summary": "Great place to work."}'

        # act
        review_id = 1
        processor.save_insights(review_id, fake_result)

        # assert
        assert mock_cursor.execute.called





