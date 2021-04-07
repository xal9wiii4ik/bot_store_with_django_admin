from rest_framework.serializers import ValidationError

from apps.product.models import Product


def verification_product_name_and_check_quantity(product_name: str) -> str:
    """Validation product on exist and check quantity"""

    product = Product.objects.filter(name=product_name)
    if len(product) != 0:
        if product[0].quantity >= 1:
            return product_name
    raise ValidationError('At the moment the product is out of stock')
