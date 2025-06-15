import psycopg2
import json
from db.connection import get_psql_connection
import logging

logger = logging.getLogger("uvicorn.error")

psql = get_psql_connection()


async def save_user_answer_to_psql(user_id, answer):
    if psql is None:
        logger.warning("Database connection is not available. Skipping save operation.")
        return

    try:
        answer_json = json.dumps({"answer": answer})
        with psql.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO user_answers (user_id, answer)
                VALUES (%s, %s);
                """,
                (user_id, answer_json)
            )
            psql.commit()
            logger.info(f"User answer saved to database for user_id: {user_id}")
    except psycopg2.Error as e:
        logger.error(f"Failed to save user answer to database: {e}")
        raise


async def get_user_answers_from_psql(user_id, limit):
    if psql is None:
        logger.warning("Database connection is not available.")
        return []

    try:
        with psql.cursor() as cursor:
            cursor.execute(
                """
                SELECT answer, created_at 
                FROM user_answers 
                WHERE user_id = %s 
                ORDER BY created_at DESC 
                LIMIT 5;
                """,
                (user_id, limit)
            )
            results = cursor.fetchall()
            
            answers = []
            for row in results:
                answer_data = json.loads(row[0])
                answers.append({
                    "answer": answer_data["answer"],
                    "created_at": row[1].isoformat()
                })
            
            return answers
    except psycopg2.Error as e:
        logger.error(f"Failed to get user answers from database: {e}")
        raise
