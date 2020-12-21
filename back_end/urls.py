from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import SimpleRouter

from apps.product.views import (
    ProductViewSet,
    MailingProduct,
)
from apps.user_profile.views import (
    BlackListUsersViewSet,
    UsersQueueViewSet,
    AddUserFromQueue,
    RemoveUserView,
    UserProfileViewSet,
    MiddlewareBlackListUserView,
    MiddlewareRemoveBlackListUserView,
)
from apps.cart.views import PurchasesHistoryViewSet, ProductPurchaseView
from back_end import settings

router = SimpleRouter()
router.register(r'product', ProductViewSet)
router.register(r'black_list_users', BlackListUsersViewSet)
router.register(r'purchases_history', PurchasesHistoryViewSet)
router.register(r'users_queue', UsersQueueViewSet)
router.register(r'user_profile', UserProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('product_purchase/', ProductPurchaseView.as_view(), name='product_purchase'),
    path('add_user_from_queue/<int:chat_id>/', AddUserFromQueue.as_view(), name='add_user_from_queue'),
    path('remove_user/', RemoveUserView.as_view(), name='remove_user'),
    path('mailing_product/<int:id>/', MailingProduct.as_view(), name='mailing_product'),
    path('middleware_black_list/<int:chat_id>/', MiddlewareBlackListUserView.as_view(), name='middleware_black_list'),
    path('middleware_remove_black_list/<int:id>/',
         MiddlewareRemoveBlackListUserView.as_view(),
         name='middleware_remove_black_list')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
