from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services.user_question_service import save_user_question


class UserQuestionRequest(BaseModel):
    question: str


router = APIRouter()


@router.post("/users/{user_id}/question")
async def set_user_question_api(user_id: int, request: UserQuestionRequest):
    try:
        await save_user_question(user_id, request.question)
        return JSONResponse(content={"status": "ok"})
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save user question")
