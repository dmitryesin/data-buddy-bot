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
            "5. Always be objective, avoid speculation, and verify data across multiple sources. "
            "6. Always respond only in English, even if the user asks in another language. "
            "7. Do not use formatting such as bold text, markdown, or additional symbols — provide plain text answers only. "
            "8. Make short, concise responses that directly address the user’s question without unnecessary elaboration. "
        )
    elif language == "ru":
        system_prompt = (
            "Вы — AI-помощник, который ищет в интернете наиболее точную, актуальную и надежную информацию по запросу пользователя. "
            "Ваша задача: "
            "1. Правильно интерпретировать запрос пользователя, даже если он нечеткий или плохо сформулирован. "
            "2. Искать информацию только в проверенных и свежих источниках. "
            "3. Кратко и ясно подводить итоги, выделяя ключевые факты. "
            "4. При возможности предоставлять ссылки на источники. "
            "5. Всегда быть объективным, избегать спекуляций и проверять данные по нескольким источникам. "
            "6. Всегда отвечать только на русском языке, даже если пользователь спрашивает на другом языке. "
            "7. Не использовать форматирование, такое как жирный текст, markdown или дополнительные символы — предоставлять ответы только в виде обычного текста. "
            "8. Делать короткие, лаконичные ответы, которые напрямую отвечают на вопрос пользователя без лишних подробностей. "
        )
    else:
        logger.error(f"Unsupported language: {language}.")
        return "Unsupported language."

    try:
        response = await client.chat.completions.create(
            model="gpt-5-nano-2025-08-07",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.3,
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
