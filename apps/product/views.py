import requests
from django.db.models.expressions import F
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status

from apps.product.models import Product
from apps.product.serializers import ProductModelSerializer
from back_end import settings


class ProductViewSet(ModelViewSet):
    """View Set для модели продукта"""

    queryset = Product.objects.all().annotate(
        price_with_discount=F('price')-F('discount')
    )
    serializer_class = ProductModelSerializer
    permission_classes = (permissions.IsAdminUser,)


class MailingProduct(APIView):
    """Рассылка продукта"""

    def get(self, request, id: int) -> Response:
        requests.post(url=settings.URL.replace('command', f'/mailing_product {id}'))
        return Response(data={'ok': 'ok'},
                        status=status.HTTP_200_OK)
