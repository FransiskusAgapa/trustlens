import os
import logging
import psycopg2
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")

    try:
        conn = psycopg2.connect(database_url, connect_timeout=10)
        logger.info("Database connection established")
        return conn
    except psycopg2.OperationalError as e:
        logger.error("Failed to connect to database: %s", e)
        raise