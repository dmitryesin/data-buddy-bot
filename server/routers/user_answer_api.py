from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, HTTPException
from services.user_question_service import get_user_answers, process_user_question

router = APIRouter()


@router.post("/users/{user_id}/ask")
async def ask_question_api(
    user_id, question: str = Body(...), language: Optional[str] = Body("ru")
) -> Dict[str, Any]:
    try:
        answer = await process_user_question(user_id, question, language)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process question: {str(e)}"
        )


@router.get("/users/{user_id}/answers")
async def get_user_answers_api(user_id):
    try:
        answers = await get_user_answers(user_id)
        return {"answers": answers}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get user answers: {str(e)}"
        )
