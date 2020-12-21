from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.cart.models import PurchasesHistory


@admin.register(PurchasesHistory)
class PurchasesHistoryAdmin(admin.ModelAdmin):
    """Админка для истории покупок"""

    def get_image_url(self, obj: PurchasesHistory):
        """Получение ссылки на картинку для вывода в панели администратора"""

        return mark_safe(f'<img src="{obj.product.image.url}" width="80" height="80" />')

    def get_obj_name(self, obj: PurchasesHistory) -> str:
        """Получение имени продукта"""

        return obj.product.name

    def get_user_username(self, obj) -> str:
        """Получение имени пользователя"""

        return obj.user.username

    list_display = ('id', 'get_user_username', 'get_obj_name', 'get_image_url')
