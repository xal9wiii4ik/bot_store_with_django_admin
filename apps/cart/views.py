from django.db.models.expressions import F

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework import mixins, permissions, status

from apps.cart.models import PurchasesHistory
from apps.cart.serializers import PurchasesHistoryModelSerializer, ProductPurchaseSerializer
from apps.cart.services_views import add_product_to_purchase_history_and_change_quantity


class PurchasesHistoryViewSet(mixins.ListModelMixin,
                              GenericViewSet):
    """View Set for purchases history"""

    queryset = PurchasesHistory.objects.all().annotate(
        chat_id=F('user__chat_id'),
        product_name=F('product__name'),
        image_url=F('product__image'),
        price_with_discount=F('product__price')-F('product__discount')
    )
    serializer_class = PurchasesHistoryModelSerializer
    permission_classes = (permissions.IsAdminUser,)


class ProductPurchaseView(APIView):
    """View product purchases"""

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request) -> Response:
        serializer = ProductPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            add_product_to_purchase_history_and_change_quantity(data=serializer.data)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
