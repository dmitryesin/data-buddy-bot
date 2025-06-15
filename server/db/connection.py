import os
import psycopg2
from dotenv import load_dotenv
import logging

logger = logging.getLogger("uvicorn.error")

load_dotenv()


def get_psql_connection():
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_DATABASE", "postgres"),
            user=os.getenv("DB_USERNAME", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
    except psycopg2.OperationalError:
        logger.error("Failed to connect to database.")
        return None
