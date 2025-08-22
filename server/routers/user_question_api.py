from fastapi import APIRouter, HTTPException
from services.user_question_service import get_user_questions

router = APIRouter()


@router.post("/users/{user_id}/question")
async def set_user_question_api():
    return {"status": "ok"}


@router.get("/users/{user_id}/questions")
async def get_user_questions_api(user_id):
    try:
        questions = await get_user_questions(user_id)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get user questions: {str(e)}"
        )
