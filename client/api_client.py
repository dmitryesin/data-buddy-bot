import json
import os

from aiohttp import ClientSession, ClientTimeout

REQUEST_TIMEOUT = 60


async def set_user_settings(user_id, language):
    payload = {
        "language": language,
    }

    timeout = ClientTimeout(total=REQUEST_TIMEOUT)
    async with ClientSession(timeout=timeout) as session:
        async with session.post(
            f"{os.getenv('SERVER_API_URL')}/users/{user_id}/settings", params=payload
        ) as response:
            response.raise_for_status()
            return await response.text()


async def get_user_settings(user_id, language):
    timeout = ClientTimeout(total=REQUEST_TIMEOUT)
    async with ClientSession(timeout=timeout) as session:
        async with session.get(
            f"{os.getenv('SERVER_API_URL')}/users/{user_id}/settings"
        ) as response:
            if response.status == 404:
                return {
                    "language": language,
                }

            response.raise_for_status()
            text = await response.text()
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                return text
            return data


async def set_user_question(user_id, question):
    payload = {
        "question": question,
    }

    timeout = ClientTimeout(total=REQUEST_TIMEOUT)
    async with ClientSession(timeout=timeout) as session:
        async with session.post(
            f"{os.getenv('SERVER_API_URL')}/users/{user_id}/question", json=payload
        ) as response:
            response.raise_for_status()
            return await response.text()


async def ask_question(user_id, question, language):
    payload = {
        "question": question,
        "language": language,
    }

    timeout = ClientTimeout(total=REQUEST_TIMEOUT)
    async with ClientSession(timeout=timeout) as session:
        async with session.post(
            f"{os.getenv('SERVER_API_URL')}/users/{user_id}/ask", json=payload
        ) as response:
            response.raise_for_status()
            text = await response.text()
            try:
                data = json.loads(text)
                return data.get("answer", text)
            except json.JSONDecodeError:
                return text


async def get_user_answers(user_id):
    timeout = ClientTimeout(total=REQUEST_TIMEOUT)
    async with ClientSession(timeout=timeout) as session:
        async with session.get(
            f"{os.getenv('SERVER_API_URL')}/users/{user_id}/answers"
        ) as response:
            response.raise_for_status()
            text = await response.text()
            try:
                data = json.loads(text)
                return data.get("answers", [])
            except json.JSONDecodeError:
                return []


async def get_user_questions(user_id):
    timeout = ClientTimeout(total=REQUEST_TIMEOUT)
    async with ClientSession(timeout=timeout) as session:
        async with session.get(
            f"{os.getenv('SERVER_API_URL')}/users/{user_id}/questions"
        ) as response:
            response.raise_for_status()
            text = await response.text()
            try:
                data = json.loads(text)
                return data.get("questions", [])
            except json.JSONDecodeError:
                return []
