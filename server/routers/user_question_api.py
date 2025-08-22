from fastapi import APIRouter, Body, HTTPException
from services.user_question_service import get_user_questions, save_user_question

router = APIRouter()


@router.post("/users/{user_id}/question")
async def set_user_question_api(user_id, question: str = Body(..., embed=True)):
    try:
        await save_user_question(user_id, question)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to save user question: {str(e)}"
        )


@router.get("/users/{user_id}/questions")
async def get_user_questions_api(user_id):
    try:
        questions = await get_user_questions(user_id)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get user questions: {str(e)}"
        )
