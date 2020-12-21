# bot_store_with_django_admin
Bot(online store) with admin panel on django.

When user press start he waiting when u add him from admin panel. 
You can add product on django admin panel and send mailing with products or product to users from admin panel.
You can add user in black list and this user will not recieve products or new product within ban_days days
and then bot automatically will delete user from black list or you can do this in admin panel.
All commands bot will send to your chat in telegram

HOW INSTALL:
1) write commands: 
    1. pip install -r requirements.txt,
    2. python manage.py migrate
2) change .env
3) write commands: 
    1. python manage.py runserver,
    2. python app.py
