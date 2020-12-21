from datetime import datetime, timedelta

from django.test import TestCase
from django.db.models import Count

from apps.user_profile.models import BlackListUsers, UserQueue
from apps.user_profile.serializers import BlackListUsersModelSerializer, UsersQueueModelSerializer


class BlackListUsersModelSerializerTestCase(TestCase):
    """Test case для сериалайзера модели черного списка"""

    def test_ok(self):
        black_list_user = BlackListUsers.objects.create(
            chat_id=6780,
            date_ban=datetime.now().date(),
            days_ban=5,
            reason_ban='98',
        )
        black_list_user_1 = BlackListUsers.objects.create(
            chat_id=23444,
            date_ban=datetime.now().date(),
            days_ban=2,
            reason_ban='bitch',
        )

        black_list_users = BlackListUsers.objects.all().annotate(
            count_users_in_black_list=Count('chat_id')
        )
        data = BlackListUsersModelSerializer(black_list_users, many=True).data

        expected_data = [
            {
                'id': black_list_user.id,
                'chat_id': 6780,
                'date_ban': datetime.now().strftime('%Y-%m-%d'),
                'days_ban': 5,
                'expiration_date': (datetime.now().date() + timedelta(days=5)).strftime('%Y-%m-%d'),
                'reason_ban': '98',
            },
            {
                'id': black_list_user_1.id,
                'chat_id': 23444,
                'date_ban': datetime.now().strftime('%Y-%m-%d'),
                'days_ban': 2,
                'expiration_date': (datetime.now().date() + timedelta(days=2)).strftime('%Y-%m-%d'),
                'reason_ban': 'bitch',
            }
        ]
        self.assertEqual(first=expected_data, second=data)


class UsersQueueModelSerializerTestCase(TestCase):
    """Test case для сериалайзера модели очереди пользователей"""

    def test_ok(self):
        user_queue = UserQueue.objects.create(
            chat_id=6780,
            username='user',
            first_name='first_name',
            last_name='last_name',
        )
        user_queue_1 = UserQueue.objects.create(
            chat_id=23444,
            username='user_1',
            first_name='first_name_1',
            last_name='last_name_1',
        )

        users_queue = UserQueue.objects.all()
        data = UsersQueueModelSerializer(users_queue, many=True).data

        expected_data = [
            {
                'id': user_queue.id,
                'chat_id': 6780,
                'username': 'user',
                'first_name': 'first_name',
                'last_name': 'last_name',
            },
            {
                'id': user_queue_1.id,
                'chat_id': 23444,
                'username': 'user_1',
                'first_name': 'first_name_1',
                'last_name': 'last_name_1'
            }
        ]
        self.assertEqual(first=expected_data, second=data)
