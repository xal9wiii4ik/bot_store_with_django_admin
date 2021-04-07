from django.contrib.auth.hashers import make_password

from back_end.settings import PASSWORD
from apps.user_profile.models import (
    UserProfile,
    UserQueue,
    BlackListUsers
)


def change_ban_status(ban_status: bool, chat_id: int) -> None:
    """Change status of ban"""

    if not ban_status:
        user = UserProfile.objects.get(
            chat_id=BlackListUsers.objects.get(id=chat_id).chat_id
        )
    else:
        user = UserProfile.objects.get(chat_id=chat_id)
    user.banned = ban_status
    user.save()


def add_user_and_remove_from_user_queue(chat_id: int) -> None:
    """Add user and delete from queue"""

    user_in_queue = UserQueue.objects.get(chat_id=chat_id)
    UserProfile.objects.create(username=user_in_queue.username,
                               chat_id=user_in_queue.chat_id,
                               first_name=user_in_queue.first_name,
                               last_name=user_in_queue.last_name,
                               password=make_password(password=PASSWORD))
    user_in_queue.delete()


def remove_user(data: dict) -> None:
    """Remove user"""

    user = UserProfile.objects.filter(chat_id=data['chat_id'])
    if len(user) != 0:
        if user[0].banned:
            user_in_black_list = BlackListUsers.objects.get(chat_id=data['chat_id'])
            user_in_black_list.delete()
        user[0].delete()
    else:
        user_in_queue = UserQueue.objects.get(chat_id=data['chat_id'])
        user_in_queue.delete()


def verification_user(chat_id: int) -> bool:
    """Verification user in database"""

    user = UserProfile.objects.filter(chat_id=chat_id)
    if len(user) == 1:
        return False
    else:
        return True
