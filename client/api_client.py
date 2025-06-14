import json
import os

from aiohttp import ClientTimeout, ClientSession

REQUEST_TIMEOUT = 60


async def set_user_settings(user_id, language):
    payload = {
        "language": language,
    }

    timeout = ClientTimeout(total=REQUEST_TIMEOUT)
    async with ClientSession(timeout=timeout) as session:
        async with session.post(
            f"{os.getenv('CLIENT_API_URL')}/users/{user_id}/settings", params=payload
        ) as response:
            response.raise_for_status()
            return await response.text()


async def get_user_settings(user_id, language):
    timeout = ClientTimeout(total=REQUEST_TIMEOUT)
    async with ClientSession(timeout=timeout) as session:
        async with session.get(
            f"{os.getenv('CLIENT_API_URL')}/users/{user_id}/settings"
        ) as response:
            if response.status == 500:
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
