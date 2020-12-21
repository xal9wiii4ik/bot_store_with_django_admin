from apps.product.models import Product
from apps.cart.models import PurchasesHistory
from apps.user_profile.models import UserProfile


def add_product_to_purchase_history_and_change_quantity(data: dict) -> None:
    """Добавление продукта в историю покупок и изменение его колличества на складе"""

    product = Product.objects.get(name=data['product_name'])
    user_profile = UserProfile.objects.get(chat_id=data['chat_id'])
    PurchasesHistory.objects.create(user=user_profile, product=product)
    product.quantity = product.quantity - 1
    product.save()
