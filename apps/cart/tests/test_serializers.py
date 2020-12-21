from django.test import TestCase
from django.db.models.expressions import F

from apps.cart.models import PurchasesHistory
from apps.cart.serializers import PurchasesHistoryModelSerializer
from apps.product.models import Product
from apps.user_profile.models import UserProfile


class PurchasesHistoryModelSerializerTestCase(TestCase):
    """Test case для сериалайзера модели списка продуктов"""

    def test_ok(self):
        user = UserProfile.objects.create(username='user')
        user_1 = UserProfile.objects.create(username='user_1', chat_id=123)

        product = Product.objects.create(
            name='product',
            price=123.78,
            description='description',
            quantity=98,
        )
        product_1 = Product.objects.create(
            name='product_1',
            price=97.20,
            discount=22.20,
            description='description_1',
        )

        purchase = PurchasesHistory.objects.create(
            user=user,
            product=product_1
        )
        purchase_1 = PurchasesHistory.objects.create(
            user=user_1,
            product=product
        )

        purchases = PurchasesHistory.objects.all().annotate(
            chat_id=F('user__chat_id'),
            product_name=F('product__name'),
            image_url=F('product__image'),
            price_with_discount=F('product__price') - F('product__discount')
        )
        data = PurchasesHistoryModelSerializer(purchases, many=True).data

        expected_data = [
            {
                'id': purchase.id,
                'chat_id': 0,
                'product_name': product_1.name,
                'price_with_discount': '75.00',
                'image_url': str(product_1.image)
            },
            {
                'id': purchase_1.id,
                'chat_id': 123,
                'product_name': product.name,
                'price_with_discount': '123.78',
                'image_url': str(product.image)
            }
        ]
        self.assertEqual(first=expected_data, second=data)
