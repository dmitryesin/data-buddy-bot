from fastapi import FastAPI
from routers.user_settings_api import router as user_settings_router

app = FastAPI()
app.include_router(user_settings_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
