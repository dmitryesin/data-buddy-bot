from fastapi import APIRouter, HTTPException, Body

from services.user_question_service import save_user_question, get_user_questions


router = APIRouter()


@router.post("/users/{user_id}/question")
async def set_user_question_api(user_id, question: str = Body(..., embed=True)):
    try:
        await save_user_question(user_id, question)
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save user question")


@router.get("/users/{user_id}/questions")
async def get_user_questions_api(user_id):
    try:
        questions = await get_user_questions(user_id)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get user questions: {str(e)}"
        )
