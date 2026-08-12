import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    # Read DATABASE_URL from environment using os.getenv()
    # Connect using psycopg2.connect()
    # Return the connection
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("Hey, DATABASE_URL environment variable is not set.")

    return psycopg2.connect(database_url)

