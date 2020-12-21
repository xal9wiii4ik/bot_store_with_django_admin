from django.test import TestCase

from apps.product.models import Product
from apps.cart.services_views import add_product_to_purchase_history_and_change_quantity
from apps.user_profile.models import UserProfile


class ServicesViewsTestCase(TestCase):
    """Test case для бизнес логики views"""

    def setUp(self) -> None:
        self.user = UserProfile.objects.create(username='user', chat_id=123)

        self.product = Product.objects.create(
            name='product',
            price=123.78,
            description='description',
            quantity=98,
        )

    def test_add_product_to_purchase_history_and_change_quantity(self) -> None:
        """Тест для добавление продукта в историю покупок и изменение его колличества на складе"""

        self.assertEqual(first=98, second=self.product.quantity)
        data = {
            'product_name': self.product.name,
            'chat_id': self.user.chat_id
        }
        add_product_to_purchase_history_and_change_quantity(data=data)
        self.product.refresh_from_db()
        self.assertEqual(first=97, second=self.product.quantity)
