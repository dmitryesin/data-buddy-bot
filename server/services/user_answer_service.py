import aiohttp
import os
import logging

logger = logging.getLogger("uvicorn.error")

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}


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

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 500
    }

    proxy = "http://127.0.0.1:10808"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENAI_API_URL, headers=HEADERS, json=payload, proxy=proxy) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"LLM API error: {response.status}. Details: {error_text}")
                    return "Request error."

                data = await response.json()
                try:
                    answer = data["choices"][0]["message"]["content"]
                    logger.info(f"LLM response received successfully for question: {question[:50]}...")
                    return answer
                except (KeyError, IndexError) as e:
                    logger.error(f"Response parsing error: {str(e)}. Raw response: {data}")
                    return "Response parsing error."
                    
    except Exception as e:
        logger.error(f"LLM connection error: {str(e)}")
        return "Connection error."
