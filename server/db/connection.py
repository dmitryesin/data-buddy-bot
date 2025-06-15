import os
import psycopg2
from dotenv import load_dotenv
import logging

logger = logging.getLogger("uvicorn.error")

load_dotenv()


def get_psql_connection():
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
    except psycopg2.OperationalError:
        logger.error("Failed to connect to database.")
        return None
