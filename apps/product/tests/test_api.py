import json

from django.contrib.auth.hashers import make_password

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from apps.user_profile.models import UserProfile
from apps.product.models import Product


class ProductApiTestCase(APITestCase):
    """Api test case для view продукта"""

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

    def test_get_staff(self) -> None:
        """Тест для получения списка продуктов администратором"""

        url = reverse('product-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)

    def test_get_not_staff(self) -> None:
        """Тест для получения списка продуктов не администратором"""

        url = reverse('product-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_create_staff(self) -> None:
        """Тест для создания продукта администратором"""

        self.assertEqual(first=2, second=Product.objects.all().count())
        url = reverse('product-list')
        data = {
            'name': 'create product',
            'price': '78.78',
            'discount': '23.36',
            'description': 'create description',
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(first=status.HTTP_201_CREATED, second=response.status_code)
        self.assertEqual(first='create product', second=Product.objects.get(id=3).name)
        self.assertEqual(first=3, second=Product.objects.all().count())

    def test_create_not_staff(self) -> None:
        """Тест для создания продукта не администратором"""

        self.assertEqual(first=2, second=Product.objects.all().count())
        url = reverse('product-list')
        data = {
            'name': 'create product',
            'price': '78.78',
            'discount': '23.36',
            'description': 'create description',
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.assertEqual(first=2, second=Product.objects.all().count())

    def test_update_staff(self) -> None:
        """Тест для обновления продукта администратором"""

        self.assertEqual(first='product', second=self.product.name)
        url = reverse('product-detail', args=(self.product.id,))
        data = {
            'name': 'update product'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(path=url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.product.refresh_from_db()
        self.assertEqual(first='update product', second=self.product.name)

    def test_update_not_staff(self) -> None:
        """Тест для обновления продукта не администратором"""

        self.assertEqual(first='product', second=self.product.name)
        url = reverse('product-detail', args=(self.product.id,))
        data = {
            'name': 'update product'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.patch(path=url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.product.refresh_from_db()
        self.assertEqual(first='product', second=self.product.name)

    def test_delete_staff(self) -> None:
        """Тест для удаления продукта администратором"""

        self.assertEqual(first=2, second=Product.objects.all().count())
        url = reverse('product-detail', args=(self.product.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url, content_type='application/json')
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.assertEqual(first=1, second=Product.objects.all().count())

    def test_delete_not_staff(self) -> None:
        """Тест для удаления продукта не администратором"""

        self.assertEqual(first=2, second=Product.objects.all().count())
        url = reverse('product-detail', args=(self.product.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url, content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.assertEqual(first=2, second=Product.objects.all().count())
