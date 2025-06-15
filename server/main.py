import os
from fastapi import FastAPI
from routers.user_settings_api import router as user_settings_router
from routers.user_question_api import router as user_question_router
from routers.user_answer_api import router as user_answer_router

app = FastAPI()
app.include_router(user_settings_router)
app.include_router(user_question_router)
app.include_router(user_answer_router)

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port)
