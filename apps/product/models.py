import os

from django.db import models


def get_unique_image_url(product_name: str, image_name: str) -> os or str:
    """Изменение имени фотографии"""

    image_extension = image_name.split('.')[-1]
    rename = product_name + '.' + image_extension
    if rename != image_name.split('/')[-1]:
        return os.path.join(rename)
    else:
        return image_name


class Product(models.Model):
    """Модель продукта"""

    name = models.CharField(max_length=40, verbose_name='Имя продукта', unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена продукта')
    discount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Скидка на продукт',
                                   null=True, blank=True, default=0)
    description = models.TextField(max_length=400, verbose_name='Описание продукта')
    quantity = models.IntegerField(verbose_name='Колличество продукта', default=1)
    image = models.ImageField(upload_to='products_images', verbose_name='Фотография продукта', null=True, blank=True)

    def __str__(self):
        return f'id: {self.pk}, name: {self.name}'

    def save(self, *args, **kwargs):
        if self.image:
            self.image.name = get_unique_image_url(product_name=self.name, image_name=self.image.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
