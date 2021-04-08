# bot_store_with_django_admin
Bot(online store) with admin panel on django and with custom celery using all the beauty of asyncio and states. 

When user press start he waiting when u add him from admin panel. 
You can add product on django admin panel and send mailing with products or product to users from admin panel.
You can add user in black list and this user will not recieve products or new product within ban_days days
and then bot automatically will delete user from black list or you can do this in admin panel.
All commands bot will send to your chat in telegram

# main libraries:
1) aiogram
2) aiohttp
3) djangorestframework
4) djangorestframework-simplejwt
5) requests
6) smtp
7) MySQL

# date the code was written: 21.12.2020


P.S. Architacture on all bot projects i took from here: https://github.com/Latand/aiogram-bot-template    
