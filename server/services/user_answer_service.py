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
            "You are an expert in Russian business law. "
            "Answer only questions related to registering an LLC in Russia. "
            "If the question is unrelated, politely decline. "
            "Keep answers concise for use in a chat. "
            "Always respond in English, even if the user's question is in another language."
        )
    elif language == "ru":
        system_prompt = (
            "Ты — эксперт по российскому бизнес-праву. "
            "Отвечай только на вопросы, связанные с открытием ООО в России. "
            "Если вопрос не касается этой темы, вежливо сообщи об этом и откажись отвечать. "
            "Отвечай кратко, так как ответы будут использоваться в чате. "
            "Всегда отвечай на русском языке, даже если вопрос задан на другом языке."
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
