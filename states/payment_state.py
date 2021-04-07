from aiogram.dispatcher.filters.state import StatesGroup, State


class PaymentState(StatesGroup):
    """State of payment"""

    EnterQuantity = State()
    Payment = State()
