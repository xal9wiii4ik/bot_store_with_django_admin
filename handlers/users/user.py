import json

import requests
from aiogram import types

from back_end import settings
from loader import dp


@dp.message_handler()
async def question_not_mailing(message: types.Message) -> None:
    """MEssage about user in black list"""

    text = ''
    if message.text.lower() == 'почему не приходят продукты?':
        response = requests.get(url=settings.SERVER_HOST.replace('path', f'black_list_users'),
                                headers={
                                    'Authorization': settings.AUTHORIZATION_TOKEN
                                }, params=None)
        users_in_black_list = json.loads(response._content.decode('utf-8'))
        for user in users_in_black_list:
            if user['chat_id'] == message.from_user.id:
                text += f'Потому что ты забанен(0\nДата истечения бана: {user["expiration_date"]}\n' \
                       f'Причина такова: {user["reason_ban"]}'
    if message.text.lower() == 'мои покупки':
        response = requests.get(url=settings.SERVER_HOST.replace('path', f'purchases_history'),
                                headers={
                                    'Authorization': settings.AUTHORIZATION_TOKEN
                                }, params=None)
        purchase_history = json.loads(response._content.decode('utf-8'))
        for purchase in purchase_history:
            if purchase['chat_id'] == message.from_user.id:
                text += f'Название продукта: {purchase["product_name"]}\n' \
                        f'Цена: {purchase["price_with_discount"]}'
    await message.answer(text=text)
