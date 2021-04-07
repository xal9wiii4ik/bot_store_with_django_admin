from rest_framework import serializers

from apps.product.models import Product


class ProductModelSerializer(serializers.ModelSerializer):
    """Model Serializer for Product"""

    price_with_discount = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name',
                  'image', 'price',
                  'discount', 'price_with_discount',
                  'description', 'quantity']
