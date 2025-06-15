import psycopg2
from db.connection import get_psql_connection
import logging

logger = logging.getLogger("uvicorn.error")

psql = get_psql_connection()
DEFAULT_LANGUAGE = "en"


async def save_user_settings_to_psql(user_id: int, user_settings: dict):
    if psql is None:
        logger.warning("Database connection is not available. Skipping save operation.")
        return

    try:
        with psql.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (id, language)
                VALUES (%s, %s)
                ON CONFLICT (id) DO UPDATE
                SET language = EXCLUDED.language;
                """,
                (
                    user_id,
                    user_settings.get('language', DEFAULT_LANGUAGE),
                )
            )
            psql.commit()
    except psycopg2.Error as e:
        logger.error(f"Failed to save user settings to database: {e}")
        raise


async def get_user_settings_from_psql(user_id: int) -> dict:
    if psql is None:
        logger.warning("Database connection is not available. Returning default user settings.")
        return {'language': DEFAULT_LANGUAGE}

    try:
        with psql.cursor() as cursor:
            cursor.execute(
                """
                SELECT language
                FROM users
                WHERE id = %s;
                """,
                (user_id,)
            )
            result = cursor.fetchone()
            if result:
                return {'language': result[0]}
    except psycopg2.Error as e:
        logger.error(f"Failed to fetch user settings from database: {e}")
        raise

    return {'language': DEFAULT_LANGUAGE}
