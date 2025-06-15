import psycopg2
import json
from db.connection import get_psql_connection
import logging

logger = logging.getLogger("uvicorn.error")

psql = get_psql_connection()


async def save_user_question_to_psql(user_id: int, question: str):
    if psql is None:
        logger.warning("Database connection is not available. Skipping save operation.")
        return

    try:
        question_json = json.dumps({"question": question})
        with psql.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO user_questions (user_id, question)
                VALUES (%s, %s);
                """,
                (user_id, question_json)
            )
            psql.commit()
    except psycopg2.Error as e:
        logger.error(f"Failed to save user question to database: {e}")
        raise
