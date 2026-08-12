from app.services.analyze import analyze_review
from app.database import get_connection
import json

class ReviewProcessor():
    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()

    def fetch_unprocessed_reviews(self):
        # fetch reviews from the database that have not been processed yet
        self.cur.execute("""
            SELECT r.id, r.content
            FROM reviews r
            LEFT JOIN review_insights ri 
            ON r.id = ri.review_id
            WHERE ri.review_id IS NULL
            LIMIT 50
        """)
        return self.cur.fetchall()

    def save_insights(self,review_id, insights):
        insights_dict = json.loads(insights)
        sentiment_label = insights_dict.get("sentiment_label")
        sentiment_score = insights_dict.get("sentiment_score")
        themes = json.dumps(insights_dict.get("themes"))
        department_tag = insights_dict.get("department_tag")
        summary = insights_dict.get("summary")

        self.cur.execute("""
            INSERT INTO review_insights (review_id, sentiment_label, sentiment_score, themes, department_tag, summary)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (review_id, sentiment_label, sentiment_score, themes, department_tag, summary))

    def run(self):
        reviews = self.fetch_unprocessed_reviews()
        for review in reviews:
            review_id = review[0]
            review_text = review[1]
            insights = analyze_review(review_text)
            self.save_insights(review_id, insights)

        # commits in psycopg2
        self.conn.commit()
