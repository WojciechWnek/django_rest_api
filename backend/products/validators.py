from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from products.models import Product


def validate_title(value):
    qs = Product.objects.filter(title__iexact=value)
    if qs.exists():
        raise serializers.ValidationError(f"{value} is already a product name")
    return value

def validate_title_no_hello(value):
    if "hello" in value.lower():
        raise serializers.ValidationError(f"Hello is not allowes")
    return value

unique_product_title = UniqueValidator(queryset=Product.objects.all())