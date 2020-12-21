from django.db import models

from back_end import settings


class PurchasesHistory(models.Model):
    """Модель истории покупок"""

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    product = models.ForeignKey(to='product.Product',
                                on_delete=models.CASCADE,
                                verbose_name='Продукт')

    def __str__(self):
        return f'id: {self.pk}, user_id: {self.user.chat_id}, product: {self.product.name}'

    class Meta:
        verbose_name = 'История покупок'
        verbose_name_plural = 'История покупок'
