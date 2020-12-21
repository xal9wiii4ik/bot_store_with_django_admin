from rest_framework import serializers

from apps.cart.models import PurchasesHistory
from apps.cart.servicies_serializers import verification_product_name_and_check_quantity


class PurchasesHistoryModelSerializer(serializers.ModelSerializer):
    """Model serializer для модели корзины покупок"""

    chat_id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(max_length=40, read_only=True)
    price_with_discount = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    image_url = serializers.CharField(max_length=70, read_only=True)

    class Meta:
        model = PurchasesHistory
        fields = ('id', 'chat_id', 'product_name',
                  'price_with_discount', 'image_url')


class ProductPurchaseSerializer(serializers.Serializer):
    """Serializer после отплаты продукта для добавления в список покупок"""

    product_name = serializers.CharField(max_length=40, required=True)
    chat_id = serializers.IntegerField(required=True)

    def validate_product_name(self, value: str) -> str:
        return verification_product_name_and_check_quantity(product_name=value)
