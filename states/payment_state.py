from aiogram.dispatcher.filters.state import StatesGroup, State


class PaymentState(StatesGroup):
    """Класс состояния оплаты"""

    EnterQuantity = State()
    Payment = State()
