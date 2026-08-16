
from app.database import get_connection

# put these out here risk connection timeout
# conn = get_connection()
# cur = conn.cursor()

# GET /companies → list all companies
def get_companies():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies;")
    results = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    conn.close()
    return [dict(zip(columns, row)) for row in results]

# GET /companies/{id}/reviews → reviews for a specific company
def get_reviews_by_company(company_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT * 
    FROM reviews 
    WHERE company_id = %s;""", 
    (company_id,))
    results = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    conn.close()
    return [dict(zip(columns, row)) for row in results]

# GET /companies/{id}/insights → AI insights for a specific company
def get_insights_by_company(company_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ri.*, r.created_at as review_date
        FROM review_insights ri
        JOIN reviews r ON ri.review_id = r.id
        WHERE r.company_id = %s;
    """, (company_id,))
    results = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    conn.close()

    return [dict(zip(columns, row)) for row in results]