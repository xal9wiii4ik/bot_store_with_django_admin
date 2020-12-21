from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_lazy as _

from rest_framework.reverse import reverse

from apps.user_profile.models import UserProfile, BlackListUsers, UserQueue


class UserProfileAdmin(UserAdmin):
    """Кастомная админка для пользователя"""

    def add_to_black_list(self, obj):
        """Добавление в черный список"""

        return mark_safe(f'<a href="{reverse("middleware_black_list", args=(obj.chat_id,))}">add</a>')

    list_display = ('username', 'email', 'is_staff',
                    'chat_id', 'number_purchases', 'banned',
                    'add_to_black_list')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'chat_id', 'number_purchases', 'banned')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(UserProfile, UserProfileAdmin)


@admin.register(BlackListUsers)
class BlackListModel(admin.ModelAdmin):
    """Админка для черного списка пользователей"""

    def remove_from_black_list(self, obj):
        """Удаление из черного списка"""

        return mark_safe(f'<a href="{reverse("middleware_remove_black_list", args=(obj.id,))}">remove</a>')

    list_display = ('id', 'chat_id', 'date_ban', 'days_ban',
                    'expiration_date', 'reason_ban', 'remove_from_black_list')


@admin.register(UserQueue)
class UserQueueModel(admin.ModelAdmin):
    """Админка для очереди пользователей"""

    def button_add_user(self, obj):
        """Кнопки добавить пользователя"""

        return mark_safe(f'<a href="{reverse("add_user_from_queue", args=(obj.chat_id,))}">add</a>')

    list_display = ('id', 'chat_id', 'username', 'first_name', 'last_name', 'button_add_user')
