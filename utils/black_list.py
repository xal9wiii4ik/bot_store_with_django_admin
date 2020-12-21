import json
import requests

from datetime import datetime

from back_end import settings


async def remove_user_from_black_list() -> None:
    """Удаление пользователя из черного списка"""

    present_date = datetime.now().strftime('%Y-%m-%d')
    response = requests.get(url=settings.SERVER_HOST.replace('path', f'black_list_users'),
                            headers={
                                'Authorization': settings.AUTHORIZATION_TOKEN
                            }, params=None)
    users_in_black_list = json.loads(response._content.decode('utf-8'))
    for user in users_in_black_list:
        if user['expiration_date'] == present_date:
            requests.delete(url=settings.SERVER_HOST.replace('path', f'black_list_users/{int(user["id"])}'),
                            headers={
                                'Authorization': settings.AUTHORIZATION_TOKEN
                            }, params=None)
