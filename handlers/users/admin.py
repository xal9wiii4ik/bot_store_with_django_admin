import json

import requests

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, PreCheckoutQuery
from aiogram.utils.callback_data import CallbackData

from loader import dp
from back_end import settings
from states.payment_state import PaymentState

buy_item = CallbackData("buy", "product_id")


@dp.message_handler(commands=['add_user'])
async def add_user(message: types.Message):
    if message.from_user.id == settings.ADMIN_ID:
        await message.answer(text='ok')
        await dp.bot.send_message(chat_id=int(message.text.split()[-1]),
                                  text='Администратор добавил вас '
                                       'приносим извинения за ожидание')


@dp.message_handler(commands=['mailing_products'])
async def mailing_products(message: types.Message):
    """Mailing product"""

    if message.from_user.id == settings.ADMIN_ID:
        response = requests.get(url=settings.SERVER_HOST.replace('path', 'product'),
                                headers={
                                    'Authorization': settings.AUTHORIZATION_TOKEN
                                }, params=None)
        products = json.loads(response._content.decode('utf-8'))

        response = requests.get(url=settings.SERVER_HOST.replace('path', 'user_profile'),
                                headers={
                                    'Authorization': settings.AUTHORIZATION_TOKEN
                                }, params=None)
        user_profiles = json.loads(response._content.decode('utf-8'))

        for product in products:
            for user_profile in user_profiles:
                if not user_profile['banned'] and user_profile['chat_id'] != 0:
                    text = f'Есть такой продут):\n Навзание: {product["name"]}\n Цена: {product["price"]}\n ' \
                           f'Описание: {product["description"]}\n image: {product["image"]}'
                    if product['discount'] != '0.00':
                        text += f'Кста чуть не забыл.\n На него сейчас действует скидка: {product["discount"]})\n ' \
                                f'Тогда цена получается: {product["price_with_discount"]}'
                    markup = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Купить",
                                callback_data=buy_item.new(product_id=product['id'])
                            )
                        ]
                    ])
                    await dp.bot.send_message(chat_id=user_profile['chat_id'],
                                              text=text, reply_markup=markup)


@dp.callback_query_handler(buy_item.filter())
async def buying_product(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Buy product"""

    await call.message.edit_reply_markup()
    product_id = callback_data.get("product_id")
    await dp.bot.send_message(chat_id=call.from_user.id, text='Enter quantity(number)')
    await PaymentState.EnterQuantity.set()
    await state.update_data(
        product_id=product_id
    )


@dp.message_handler(regexp=r"^(\d+)$", state=PaymentState.EnterQuantity)
async def enter_quantity(message: types.Message, state: FSMContext):
    """Enter quantity product"""

    quantity = int(message.text)
    await state.update_data(
        quantity=quantity
    )
    await PaymentState.Payment.set()
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='yes', callback_data='yes'
                )
            ]
        ]
    )
    await dp.bot.send_message(chat_id=message.from_user.id,
                              text=f'Quantity = {quantity}',
                              reply_markup=markup)


@dp.message_handler(state=PaymentState.EnterQuantity)
async def not_quantity(message: types.Message):
    """check quantity"""

    await message.answer('Неверное значение, введите число!')


@dp.callback_query_handler(text_contains='yes', state=PaymentState.Payment)
async def approval(call: CallbackQuery, state: FSMContext):
    """Buying process"""

    await call.message.edit_reply_markup()
    await dp.bot.send_message(chat_id=settings.ADMIN_ID, text='Enter Payment')
    data = await state.get_data()
    response = requests.get(
        url=settings.SERVER_HOST.replace('path', f'product/{data["product_id"]}'),
        headers={
            'Authorization': settings.AUTHORIZATION_TOKEN
        }, params=None)
    product = json.loads(response._content.decode('utf-8'))
    amount = int(float(product['price_with_discount']) * 10000) * data['quantity']
    await dp.bot.send_invoice(chat_id=call.from_user.id,
                              title=product['name'],
                              description=product['description'],
                              currency='rub',
                              prices=[
                                  types.LabeledPrice(label=product['name'],
                                                     amount=amount)
                              ],
                              provider_token=settings.PAYMENT_PROVIDER_TOKEN,
                              need_name=True,
                              need_phone_number=True,
                              need_email=True,
                              need_shipping_address=True,
                              start_parameter='time-machine-example',
                              payload='some-invoice-payload-for-our-internal-use')
    await state.update_data(product_name=product['name'])
    await PaymentState.Payment.set()


@dp.pre_checkout_query_handler(state=PaymentState.Payment)
async def checkout(query: PreCheckoutQuery, state: FSMContext):
    """After buy product"""

    await dp.bot.answer_pre_checkout_query(query.id, True)
    data = await state.get_data()
    print(query.order_info)
    requests.post(url=settings.SERVER_HOST.replace('path', 'product_purchase'),
                  json={
                      'product_name': data['product_name'],
                      'chat_id': query.from_user.id
                  },
                  headers=settings.HEADERS, params=None)
    await state.reset_state()
    await dp.bot.send_message(query.from_user.id, "Спасибо за покупку")


@dp.message_handler(commands=['mailing_product'])
async def mailing_products(message: types.Message):
    """Mailing product"""

    if message.from_user.id == settings.ADMIN_ID:
        response = requests.get(
            url=settings.SERVER_HOST.replace('path', f'product/{int(message.text.split()[-1])}'),
            headers={
                'Authorization': settings.AUTHORIZATION_TOKEN
            }, params=None)
    product = json.loads(response._content.decode('utf-8'))
    response = requests.get(url=settings.SERVER_HOST.replace('path', 'user_profile'),
                            headers={
                                'Authorization': settings.AUTHORIZATION_TOKEN
                            }, params=None)
    user_profiles = json.loads(response._content.decode('utf-8'))
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Купить",
                callback_data=buy_item.new(product_id=product['id'])
            )
        ]
    ])
    text = f'Есть такой продут):\nНавзание: {product["name"]}\nЦена: {product["price"]}\n' \
           f'Описание: {product["description"]}\nimage: {product["image"]}'
    if product['discount'] != '0.00':
        text += f'Кста чуть не забыл.\n На него сейчас действует скидка: ' \
                f'{product["discount"]})\n Тогда цена получается: {product["price_with_discount"]}'

        for user_profile in user_profiles:
            if not user_profile['banned'] and user_profile['chat_id'] != 0:
                await dp.bot.send_message(chat_id=user_profile['chat_id'],
                                          text=text, reply_markup=markup)
