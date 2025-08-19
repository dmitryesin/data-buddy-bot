import logging
import os

from openai import AsyncOpenAI

logger = logging.getLogger("uvicorn.error")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")

client = AsyncOpenAI(base_url=OPENAI_API_URL, api_key=OPENAI_API_KEY)


async def ask_llm(question, language):
    if language == "en":
        system_prompt = (
            "You are an AI assistant that searches the entire internet for the most accurate, up-to-date, and reliable information based on the user’s query. "
            "Your task is to: "
            "1. Correctly interpret the user’s query, even if it is vague or poorly formulated. "
            "2. Search for information only in verified and recent sources. "
            "3. Summarize the findings concisely and clearly, highlighting key facts. "
            "4. Provide links to sources whenever possible. "
            "5. Always be objective, avoid speculation, and verify data across multiple sources."
        )
    elif language == "ru":
        system_prompt = (
            "Ты — AI-ассистент, который ищет самую точную, актуальную и надежную информацию в интернете по запросу пользователя. "
            "Твоя задача: "
            "1. Правильно интерпретировать запрос пользователя, даже если он сформулирован нечетко. "
            "2. Искать информацию только в проверенных и свежих источниках."
            "3. Кратко и понятно суммировать найденное, выделяя ключевые факты."
            "4. По возможности предоставлять ссылки на источники."
            "5. Всегда быть объективным, избегать домыслов и проверять данные по нескольким источникам."
        )
    else:
        logger.error(f"Unsupported language: {language}.")
        return "Unsupported language."

    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.7,
            top_p=0.9,
            max_tokens=500,
        )

        answer = response.choices[0].message.content
        logger.info(
            f"LLM response received successfully for question: {question[:50]}..."
        )
        return answer

    except Exception as e:
        logger.error(f"LLM API error: {str(e)}")
        return "Connection or API error."
