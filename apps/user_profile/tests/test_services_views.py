from datetime import datetime

from django.test import TestCase

from apps.user_profile.models import (
    UserQueue,
    UserProfile,
    BlackListUsers
)
from apps.user_profile.services_views import (
    add_user_and_remove_from_user_queue,
    remove_user
)


class ServicesViewsTestCase(TestCase):
    """Test case для бизнес логики views"""

    def setUp(self) -> None:
        self.user = UserProfile.objects.create(username='user2', chat_id=2222)
        self.user_1 = UserProfile.objects.create(username='user1', chat_id=777, banned=True)

        self.black_list_user = BlackListUsers.objects.create(
            chat_id=777,
            date_ban=datetime.now().date(),
            days_ban=5,
            reason_ban='98',
        )

        self.user_queue = UserQueue.objects.create(
            chat_id=2222,
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

    def test_add_user_and_remove_from_user_queue(self) -> None:
        """Тест для добавления пользователя и удаление его из очереди"""

        self.assertEqual(2, UserProfile.objects.all().count())
        self.assertEqual(2, UserQueue.objects.all().count())
        add_user_and_remove_from_user_queue(chat_id=2222)
        self.assertEqual(1, UserQueue.objects.all().count())
        self.assertEqual(3, UserProfile.objects.all().count())

    def test_remove_user(self) -> None:
        """Удаление пользователя без блокировки"""

        self.assertEqual(1, BlackListUsers.objects.all().count())
        self.assertEqual(2, UserProfile.objects.all().count())
        self.assertEqual(2, UserQueue.objects.all().count())
        remove_user(data={'chat_id': 777})
        self.assertEqual(2, UserQueue.objects.all().count())
        self.assertEqual(0, BlackListUsers.objects.all().count())

    def test_remove_user_with_ban(self) -> None:
        """Удаление пользователя с блокировкой"""

        self.assertEqual(1, BlackListUsers.objects.all().count())
        self.assertEqual(2, UserProfile.objects.all().count())
        self.assertEqual(2, UserQueue.objects.all().count())
        remove_user(data={'chat_id': 777})
        self.assertEqual(2, UserQueue.objects.all().count())
        self.assertEqual(1, UserProfile.objects.all().count())
        self.assertEqual(0, BlackListUsers.objects.all().count())

    def test_remove_user_from_queue(self) -> None:
        """Удаление пользователя из очереди"""

        self.assertEqual(1, BlackListUsers.objects.all().count())
        self.assertEqual(2, UserProfile.objects.all().count())
        self.assertEqual(2, UserQueue.objects.all().count())
        remove_user(data={'chat_id': 6780})
        self.assertEqual(1, UserQueue.objects.all().count())
        self.assertEqual(2, UserProfile.objects.all().count())
        self.assertEqual(1, BlackListUsers.objects.all().count())
