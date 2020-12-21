from django.test import TestCase
from django.db.models.expressions import F

from apps.product.models import Product
from apps.product.serializers import ProductModelSerializer


class ProductModelSerializerTestCase(TestCase):
    """Test case для сериалайзера модели продукта"""

    def test_ok(self):
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

        products = Product.objects.all().annotate(
            price_with_discount=F('price') - F('discount')
        )
        data = ProductModelSerializer(products, many=True).data

        expected_data = [
            {
                'id': product.id,
                'name': 'product',
                'image': None,
                'price': '123.78',
                'discount': '0.00',
                'price_with_discount': '123.78',
                'description': 'description',
                'quantity': 98,
            },
            {
                'id': product_1.id,
                'name': 'product_1',
                'image': None,
                'price': '97.20',
                'discount': '22.20',
                'price_with_discount': '75.00',
                'description': 'description_1',
                'quantity': 1,
            }
        ]
        self.assertEqual(first=expected_data, second=data)
