from app.database import get_connection
import json
import heapq
from collections import Counter

class InsightEngine:
    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()

    def fetch_all_themes(self):
        self.cur.execute("""
            SELECT themes, department_tag
            FROM review_insights
        """)
        return self.cur.fetchall()

    def rank_themes(self, themes_by_department):
        result = {}
        for department, themes in themes_by_department.items():
            counter = Counter(themes)
            result[department] = heapq.nlargest(5, counter.items(), key=lambda x: x[1])
        return result

    def run(self):
        themes_with_departments = self.fetch_all_themes()
        themes_by_departments = {}

        for themes, department_tag in themes_with_departments:
            if department_tag not in themes_by_departments:
                themes_by_departments[department_tag] = []
            themes_by_departments[department_tag].extend(themes)

        ranked = self.rank_themes(themes_by_departments)
        return ranked