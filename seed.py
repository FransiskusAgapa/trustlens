import csv, os
from app.database import get_connection

def seed_database_from_csv(csv_file_path):
    # connect to the database
    conn = get_connection()
    cur = conn.cursor()

    # for dev we limit companies to 5
    seen_companies = set()
    MAX_COMPANIES = 5

    # open the CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            company_name = row['firm']
            if company_name not in seen_companies:
                if len(seen_companies) >= MAX_COMPANIES:
                    continue
                seen_companies.add(company_name)

            pros = row['pros']
            cons = row['cons']
            content = f"Pros: {pros} Cons: {cons}"
            rating = round(float(row['overall_rating'])) if row['overall_rating'] else None
            review_date = row['date_review'] if row['date_review'] else None

            # execute 1: insert into COMPANIES table
            cur.execute("""
                INSERT INTO companies (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            """, (company_name,))
            
            # execute 2: get the company_id back from COMPANIES table
            cur.execute("""
                SELECT id FROM companies WHERE name = %s
            """, (company_name,))
            company_id = cur.fetchone()[0]

            cur.execute("""
                SELECT id FROM reviews WHERE company_id = %s AND content = %s
            """, (company_id, content))
            if cur.fetchone() is None:
                cur.execute("""
                    INSERT INTO reviews (company_id, content, rating, created_at)
                    VALUES (%s, %s, %s, %s)
                """, (company_id, content, rating, review_date))

    # commit at the end
    conn.commit()   

if __name__ == "__main__":
    print("\n Start Seeding...")
    csv_file_path = "data/glassdoor_reviews.csv"
    seed_database_from_csv(csv_file_path)
    print("\n Done Seeding.")