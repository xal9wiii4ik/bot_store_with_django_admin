import json

from django.contrib.auth.hashers import make_password

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from apps.user_profile.models import UserProfile
from apps.product.models import Product
from apps.cart.models import PurchasesHistory


class PurchasesHistoryApiTestCase(APITestCase):
    """Api test case для view списка продуктов"""

    def setUp(self) -> None:
        self.url = reverse('token')
        self.password = '123123123'

        self.user = UserProfile.objects.create(username='user', password=make_password(self.password),
                                               is_staff=True)
        data = {
            'username': self.user.username,
            'password': self.password
        }
        json_data = json.dumps(data)
        self.token = 'Token ' + self.client.post(path=self.url, data=json_data,
                                                 content_type='application/json').data['access']

        self.user_1 = UserProfile.objects.create(username='user_1', password=make_password(self.password))
        data_1 = {
            'username': self.user_1.username,
            'password': self.password
        }
        json_data_1 = json.dumps(data_1)
        self.token_1 = 'Token ' + self.client.post(path=self.url, data=json_data_1,
                                                   content_type='application/json').data['access']

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
            quantity=65,
        )

        self.purchase = PurchasesHistory.objects.create(
            user=self.user,
            product=self.product
        )
        self.purchase_1 = PurchasesHistory.objects.create(
            user=self.user,
            product=self.product_1
        )

    def test_get_staff(self) -> None:
        """Тест для получения списка покупок администратором"""

        url = reverse('purchaseshistory-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)

    def test_get_not_staff(self) -> None:
        """Тест для получения списка покупок не администратором"""

        url = reverse('purchaseshistory-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_create_staff(self) -> None:
        """Тест для добавления в список покупок администратором"""

        self.assertEqual(first=2, second=PurchasesHistory.objects.all().count())
        url = reverse('purchaseshistory-list')
        data = {
            'user': self.user_1.id,
            'product': self.product_1.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(first=status.HTTP_405_METHOD_NOT_ALLOWED, second=response.status_code)
        self.assertEqual(first=2, second=PurchasesHistory.objects.all().count())
