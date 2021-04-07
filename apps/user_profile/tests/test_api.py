import json

from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from apps.user_profile.models import UserProfile, UserQueue
from apps.user_profile.models import BlackListUsers


class BlackListUsersApiTestCase(APITestCase):
    """Api test case for view black list"""

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

        self.user_3 = UserProfile.objects.create(username='user1', chat_id=777)
        self.user_4 = UserProfile.objects.create(username='user4', chat_id=6780)

        self.black_list_user = BlackListUsers.objects.create(
            chat_id=6780,
            date_ban=datetime.now().date(),
            days_ban=5,
            reason_ban='98',
        )
        self.black_list_user_1 = BlackListUsers.objects.create(
            chat_id=23444,
            date_ban=datetime.now().date(),
            days_ban=2,
            reason_ban='bitch',
        )

    def test_get_staff(self) -> None:
        """Get list (admin token)"""

        url = reverse('blacklistusers-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)

    def test_get_not_staff(self) -> None:
        """Get list (user token)"""

        url = reverse('blacklistusers-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_create_staff(self) -> None:
        """add user to list (admin token)"""

        self.assertEqual(first=2, second=BlackListUsers.objects.all().count())
        url = reverse('blacklistusers-list')
        data = {
            'chat_id': 777,
            'date_ban': '2020-12-15',
            'days_ban': 10,
            'reason_ban': '98'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(first=status.HTTP_201_CREATED, second=response.status_code)
        self.assertEqual(first=(datetime.now().date() + timedelta(days=10)).strftime('%Y-%m-%d'),
                         second=BlackListUsers.objects.get(id=3).expiration_date.strftime('%Y-%m-%d'))
        self.assertEqual(first=3, second=BlackListUsers.objects.all().count())

    def test_create_not_staff(self) -> None:
        """add user to list (user token)"""

        self.assertEqual(first=2, second=BlackListUsers.objects.all().count())
        url = reverse('blacklistusers-list')
        data = {
            'chat_id': 9876,
            'date_ban': '2020-12-15',
            'days_ban': 10,
            'reason_ban': '98'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.assertEqual(first=2, second=BlackListUsers.objects.all().count())

    def test_update_staff(self) -> None:
        """update user in list (admin token)"""

        self.assertEqual(first=(datetime.now().date() + timedelta(days=5)).strftime('%Y-%m-%d'),
                         second=self.black_list_user.expiration_date.strftime('%Y-%m-%d'))
        url = reverse('blacklistusers-detail', args=(self.black_list_user.id,))
        data = {
            'days_ban': '1'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(path=url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.black_list_user.refresh_from_db()
        self.assertEqual(first=(datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%d'),
                         second=self.black_list_user.expiration_date.strftime('%Y-%m-%d'))

    def test_update_not_staff(self) -> None:
        """update user in list (user token)"""

        url = reverse('blacklistusers-detail', args=(self.black_list_user.id,))
        data = {
            'days_ban': '1'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.patch(path=url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_delete_staff(self) -> None:
        """delete user from list (admin token)"""

        self.assertEqual(first=2, second=BlackListUsers.objects.all().count())
        url = reverse('blacklistusers-detail', args=(self.black_list_user.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url, content_type='application/json')
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.assertEqual(first=1, second=BlackListUsers.objects.all().count())

    def test_delete_not_staff(self) -> None:
        """delete user from list (user token)"""

        self.assertEqual(first=2, second=BlackListUsers.objects.all().count())
        url = reverse('blacklistusers-detail', args=(self.black_list_user.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url, content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.assertEqual(first=2, second=BlackListUsers.objects.all().count())


class UserQueueApiTestCase(APITestCase):
    """Api test case for view users queue"""

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

        self.user_queue = UserQueue.objects.create(
            chat_id=6780,
            username='user',
            first_name='first_name',
            last_name='last_name',
        )
        self.user_queue_1 = UserQueue.objects.create(
            chat_id=23444,
            username='user_1',
            first_name='first_name_1',
            last_name='last_name_1',
        )

    def test_get_staff(self) -> None:
        """Get queue (admin token)"""

        url = reverse('userqueue-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)

    def test_get_not_staff(self) -> None:
        """Get queue (user token)"""

        url = reverse('userqueue-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_create_staff(self) -> None:
        """add user to queue (admin token)"""

        self.assertEqual(first=2, second=UserQueue.objects.all().count())
        url = reverse('userqueue-list')
        data = {
            'chat_id': 1111,
            'username': 'create user',
            'first_name': 'create first_name',
            'last_name': 'create last_name',
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(first=status.HTTP_201_CREATED, second=response.status_code)
        self.assertEqual(first='create user', second=UserQueue.objects.get(id=3).username)
        self.assertEqual(first=3, second=UserQueue.objects.all().count())

    def test_create_not_staff(self) -> None:
        """add user to queue (user token)"""

        self.assertEqual(first=2, second=UserQueue.objects.all().count())
        url = reverse('userqueue-list')
        data = {
            'chat_id': 1111,
            'username': 'create user',
            'first_name': 'create first_name',
            'last_name': 'create last_name',
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.assertEqual(first=2, second=UserQueue.objects.all().count())

    def test_update_staff(self) -> None:
        """update user in queue (admin token)"""

        url = reverse('userqueue-detail', args=(self.user_queue.id,))
        data = {
            'username': 'create user'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(path=url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(first=status.HTTP_405_METHOD_NOT_ALLOWED, second=response.status_code)

    def test_delete_staff(self) -> None:
        """update user in queue (user token)"""

        self.assertEqual(first=2, second=UserQueue.objects.all().count())
        url = reverse('userqueue-detail', args=(self.user_queue.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url, content_type='application/json')
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.assertEqual(first=1, second=UserQueue.objects.all().count())

    def test_delete_not_staff(self) -> None:
        """delete user from queue (user token)"""

        self.assertEqual(first=2, second=UserQueue.objects.all().count())
        url = reverse('userqueue-detail', args=(self.user_queue.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url, content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.assertEqual(first=2, second=UserQueue.objects.all().count())
