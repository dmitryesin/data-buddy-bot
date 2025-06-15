from db.user_question_repository import (
    save_user_question_to_psql,
)
from db.user_answer_repository import (
    save_user_answer_to_psql,
    get_user_answers_from_psql,
)
from services.user_answer_service import ask_llm
import logging

logger = logging.getLogger("uvicorn.error")


async def save_user_question(user_id, question):
    await save_user_question_to_psql(user_id, question)


async def process_user_question(user_id, question, language):
    try:
        await save_user_question(user_id, question)
        logger.info(f"Question saved for user {user_id}: {question[:50]}...")
        
        answer = await ask_llm(question, language)
        
        await save_user_answer_to_psql(user_id, answer)
        logger.info(f"Answer saved for user {user_id}")
        
        return answer
    except Exception as e:
        logger.error(f"Error processing user question: {e}")
        raise


async def get_user_answers(user_id, limit):
    return await get_user_answers_from_psql(user_id, limit)
