from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.user_settings_service import get_user_settings, save_user_settings

router = APIRouter()


@router.post("/users/{user_id}/settings")
async def set_user_settings_api(user_id, language):
    try:
        await save_user_settings(user_id, {"language": language})
        return JSONResponse(content={"status": "ok"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save user settings: {str(e)}")


@router.get("/users/{user_id}/settings")
async def get_user_settings_api(user_id):
    try:
        settings = await get_user_settings(user_id)
        return JSONResponse(content=settings)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to fetch user settings: {str(e)}")
