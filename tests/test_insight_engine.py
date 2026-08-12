import pytest
from app.services.insight_engine import InsightEngine
from unittest.mock import MagicMock, patch


def test_rank_themes():
    themes_by_department = {
        "engineering": ["culture", "management", "culture", "compensation", "culture"],
        "hr": ["management", "management", "culture"]
    }

    with patch("app.services.insight_engine.get_connection", return_value=MagicMock()):
        engine = InsightEngine()
        ranked = engine.rank_themes(themes_by_department)
    
    assert ranked == {
        "engineering": [("culture", 3), ("management", 1), ("compensation", 1)],
        "hr": [("management", 2), ("culture", 1)]
    }
    