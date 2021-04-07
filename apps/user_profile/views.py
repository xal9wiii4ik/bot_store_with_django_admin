import requests

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, mixins, status

from apps.user_profile.models import BlackListUsers, UserQueue, UserProfile
from apps.user_profile.serializers import (
    BlackListUsersModelSerializer,
    UsersQueueModelSerializer,
    UserProfileModelSerializer
)
from apps.user_profile.services_views import (
    change_ban_status,
    add_user_and_remove_from_user_queue,
    remove_user,
    verification_user,
)
from back_end import settings


class UserProfileViewSet(mixins.ListModelMixin,
                         GenericViewSet):
    """view for user profile"""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer
    permission_classes = (permissions.IsAdminUser,)


class BlackListUsersViewSet(ModelViewSet):
    """View Set for BlackListUsers"""

    queryset = BlackListUsers.objects.all()
    serializer_class = BlackListUsersModelSerializer
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs):
        response = super(BlackListUsersViewSet, self).create(request, *args, **kwargs)
        change_ban_status(ban_status=True, chat_id=response.data['chat_id'])
        return response

    def destroy(self, request, *args, **kwargs):
        change_ban_status(ban_status=False, chat_id=int(request.parser_context['kwargs']['pk']))
        return super(BlackListUsersViewSet, self).destroy(request, *args, **kwargs)


class MiddlewareRemoveBlackListUserView(APIView):
    """view for MiddlewareRemoveBlackListUser"""

    def get(self, request, id):
        response = requests.delete(url=settings.SERVER_HOST.replace('path', f'black_list_users/{id}'),
                                   headers=settings.HEADERS)
        return Response(data={'ok': 'User has been removed'},
                        status=response.status_code)


class MiddlewareBlackListUserView(APIView):
    """view for MiddlewareBlackListUser"""

    def get(self, request, chat_id):
        response = requests.post(url=settings.SERVER_HOST.replace('path', 'black_list_users'),
                                 json={
                                     'chat_id': chat_id,
                                     'days_ban': 1
                                 }, headers=settings.HEADERS, params=None)
        return Response(data={'ok': 'Go to the Black list admin and add reason and change days ban'},
                        status=response.status_code)


class UsersQueueViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    """View Set for UsersQueue"""

    queryset = UserQueue.objects.all()
    serializer_class = UsersQueueModelSerializer
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs) -> Response:
        print(request.data)
        if verification_user(request.data['chat_id']):
            print(1)
            return super(UsersQueueViewSet, self).create(request, *args, **kwargs)
        else:
            return Response(data={'error': 'User already exist'},
                            status=status.HTTP_400_BAD_REQUEST)


class AddUserFromQueue(APIView):
    """View for AddUserFromQueue"""

    def get(self, request, chat_id: int) -> Response:
        add_user_and_remove_from_user_queue(chat_id=chat_id)
        requests.post(url=settings.URL.replace('command', f'/add_user {chat_id}'))
        return Response(data={'ok': 'User has been added'},
                        status=status.HTTP_201_CREATED)


class RemoveUserView(APIView):
    """view for RemoveUser"""

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request) -> Response:
        remove_user(data=request.data)
        return Response(data={'ok': 'User has been removed'})
