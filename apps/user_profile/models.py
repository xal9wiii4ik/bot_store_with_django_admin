from datetime import timedelta, datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    """UserProfile model"""

    chat_id = models.BigIntegerField(verbose_name='Айди чата пользователя', default=0, null=True)
    number_purchases = models.IntegerField(default=0, null=True, blank=True, verbose_name='Колличесвто покупок')
    banned = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'id: {self.pk}, chat_id: {self.chat_id}, username: {self.username}, ' \
               f'number purchases: {self.number_purchases}, banned: {self.banned}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class BlackListUsers(models.Model):
    """black list model"""

    chat_id = models.BigIntegerField(verbose_name='Айди чата пользователя')
    date_ban = models.DateField(auto_now_add=True, verbose_name='Дата бана')
    days_ban = models.IntegerField(verbose_name='Колличество дней бана', blank=True)
    expiration_date = models.DateField(verbose_name='Дата истечения бана', blank=True)
    reason_ban = models.CharField(max_length=500, verbose_name='Причина бана', blank=True)

    def __str__(self):
        return f'chat id: {self.chat_id}, expiration date: {self.expiration_date}, reason ban: {self.reason_ban}'

    def save(self, *args, **kwargs):
        self.expiration_date = datetime.now().date() + timedelta(days=self.days_ban)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Черный список'
        verbose_name_plural = 'Черный список пользователей'


class UserQueue(models.Model):
    """UserQueue model"""

    chat_id = models.BigIntegerField(verbose_name='Айди чата пользователя', default=0, null=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f'chat_id: {self.chat_id}, username: {self.username}, ' \
               f'first_name: {self.first_name}, last_name: {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь в очередь'
        verbose_name_plural = 'Очередь пользователей'
