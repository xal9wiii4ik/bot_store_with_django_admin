from rest_framework import serializers

from apps.user_profile.models import BlackListUsers, UserQueue, UserProfile


class BlackListUsersModelSerializer(serializers.ModelSerializer):
    """Model serializer для модели черного списка пользователей"""

    class Meta:
        model = BlackListUsers
        fields = ['id', 'chat_id',
                  'date_ban', 'days_ban',
                  'expiration_date', 'reason_ban']
        read_only_fields = ('expiration_date',)


class UserProfileModelSerializer(serializers.ModelSerializer):
    """Model serializer для модели черного списка пользователей"""

    class Meta:
        model = UserProfile
        fields = ['id', 'chat_id', 'banned']
        read_only_fields = ('expiration_date',)


class UsersQueueModelSerializer(serializers.ModelSerializer):
    """Model serializer для модели очереди пользователей"""

    class Meta:
        model = UserQueue
        fields = '__all__'
