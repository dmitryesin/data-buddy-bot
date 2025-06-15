import psycopg2
import json
from db.connection import get_psql_connection
import logging

logger = logging.getLogger("uvicorn.error")

psql = get_psql_connection()


async def save_user_question_to_psql(user_id, question):
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
                (user_id, question_json),
            )
            psql.commit()
    except psycopg2.Error as e:
        logger.error(f"Failed to save user question to database: {e}")
        raise


async def get_user_questions_from_psql(user_id):
    if psql is None:
        logger.warning("Database connection is not available.")
        return []

    try:
        with psql.cursor() as cursor:
            cursor.execute(
                """
                SELECT question, created_at 
                FROM user_questions 
                WHERE user_id = %s 
                ORDER BY created_at DESC 
                LIMIT 5;
                """,
                (user_id,),
            )
            results = cursor.fetchall()

            questions = []
            for row in results:
                if isinstance(row[0], str):
                    question_data = json.loads(row[0])
                else:
                    question_data = row[0]

                questions.append(
                    {
                        "question": question_data["question"],
                        "created_at": row[1].isoformat(),
                    }
                )

            return questions
    except psycopg2.Error as e:
        logger.error(f"Failed to get user questions from database: {e}")
        raise
