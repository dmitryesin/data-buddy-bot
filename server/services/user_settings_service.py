from db.user_settings_repository import (
    save_user_settings_to_psql,
    get_user_settings_from_psql,
)


async def save_user_settings(user_id, user_settings):
    await save_user_settings_to_psql(user_id, user_settings)


async def get_user_settings(user_id):
    return await get_user_settings_from_psql(user_id)
