from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from services.user_settings_service import save_user_settings, get_user_settings

router = APIRouter()

@router.post("/users/{user_id}/settings")
async def set_user_settings_api(user_id: int, language: str):
    try:
        await save_user_settings(user_id, {"language": language})
        return JSONResponse(content={"status": "ok"})
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save user settings")


@router.get("/users/{user_id}/settings")
async def get_user_settings_api(user_id: int):
    try:
        settings = await get_user_settings(user_id)
        return JSONResponse(content=settings)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch user settings")
