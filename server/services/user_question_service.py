from db.user_question_repository import (
    save_user_question_to_psql,
)


async def save_user_question(user_id: int, question: str):
    await save_user_question_to_psql(user_id, question)
