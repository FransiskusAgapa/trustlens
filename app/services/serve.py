
from app.database import get_connection

# GET /companies → list all companies
def get_companies():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, industry, size FROM companies;")
        results = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in results]
    finally:
        conn.close()

# GET /companies/{id}/reviews → reviews for a specific company
def get_reviews_by_company(company_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""SELECT id, company_id, department_id, content, rating, created_at 
        FROM reviews 
        WHERE company_id = %s;""", 
        (company_id,))
        results = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in results]
    finally:
        conn.close()

# GET /companies/{id}/insights → AI insights for a specific company
def get_insights_by_company(company_id):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT ri.*, r.created_at as review_date
            FROM review_insights ri
            JOIN reviews r ON ri.review_id = r.id
            WHERE r.company_id = %s
            ORDER BY r.created_at DESC;
        """, (company_id,))
        results = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in results]
    finally:
        conn.close()