from django.contrib import admin
from django.utils.safestring import mark_safe
from rest_framework.reverse import reverse

from apps.product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Display product on admin panel"""

    def button_mail_product(self, obj):
        return mark_safe(f'<a href="{reverse("mailing_product", args=(obj.id,))}">mail</a>')

    def get_image_url(self, obj: Product) -> mark_safe:
        return mark_safe(f'<img src="{obj.image.url}" width="80" height="80" />')

    list_display = ('id', 'name', 'price', 'discount', 'quantity', 'get_image_url', 'button_mail_product')
