# bot_store_with_django_admin
Bot(online store) with admin panel on django.

When user press start he waiting when u add him from admin panel. 
You can add product on django admin panel and send mailing with products or product to users from admin panel.
You can add user in black list and this user will not recieve products or new product within ban_days days
and then bot automatically will delete user from black list or you can do this in admin panel.
All commands bot will send to your chat in telegram

HOW INSTALL:
1) write command: pip install -r requirements.txt
2) change .env
3) write commands: 
    1. python manage.py migrate,
    2. python manage.py createsuperuser,
    4. python manage.py runserver,
    5. python app.py.


P.S. Architacture on all bot projects i took from here: https://github.com/Latand/aiogram-bot-template    
