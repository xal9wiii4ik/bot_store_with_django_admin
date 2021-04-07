import asyncio
import json
from datetime import datetime

import requests

from back_end import settings
from utils.black_list import remove_user_from_black_list


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


async def black_list(wait_for) -> None:
    """Work with black list"""

    while True:
        await remove_user_from_black_list()
        await asyncio.sleep(wait_for)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    dp.loop.create_task(black_list(wait_for=86400))
    executor.start_polling(dp, on_startup=on_startup)
