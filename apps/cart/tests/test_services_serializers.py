from django.test import TestCase

from rest_framework.serializers import ValidationError

from apps.product.models import Product
from apps.cart.servicies_serializers import verification_product_name_and_check_quantity
from apps.user_profile.models import UserProfile


class ServicesSerializerTestCase(TestCase):
    """Test case for services of serializer"""

    def setUp(self) -> None:
        self.user = UserProfile.objects.create(username='user', chat_id=123)

        self.product = Product.objects.create(
            name='product',
            price=123.78,
            description='description',
            quantity=98,
        )
        self.product_1 = Product.objects.create(
            name='product_1',
            price=97.20,
            discount=22.20,
            description='description_1',
            quantity=0
        )

    def test_verification_product_name_and_check_quantity_not_zero(self) -> None:
        """test for validation product on exist and check quantity"""

        verification_product_name_and_check_quantity(self.product.name)
        self.assertTrue(True)

    def test_verification_product_name_and_check_quantity_zero(self) -> None:
        """test for validation product on exist and check quantity(more the zero)"""

        try:
            verification_product_name_and_check_quantity(self.product_1.name)
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
