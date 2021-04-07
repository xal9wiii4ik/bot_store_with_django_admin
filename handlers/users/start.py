import requests

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from back_end import settings
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """command /start"""

    data = {
        'chat_id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }
    if data['username'] == None:
        data['username'] = 'debil with out username'
    response = requests.post(url=settings.SERVER_HOST.replace('path', 'users_queue'),
                             json=data, headers=settings.HEADERS, params=None)
    print(response)
    if response.status_code == 201:
        await message.answer(f'Привет! Вы оставили заявку на добавление ко мне)'
                             f'Администратор в скором времени рассмотрит вашу заявку!')
    else:
        await message.answer(f'Привет! Sorry something was wrong')

