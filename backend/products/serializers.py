from rest_framework import serializers
from rest_framework.reverse import reverse
from products.models import Product
from .validators import validate_title, validate_title_no_hello, unique_product_title
from api.serializers import UserPublicSerializer

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
    )
    title = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source="user",read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
    )
    edit_url = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(validators=[validate_title_no_hello, unique_product_title])

    class Meta:
        model = Product
        fields = [
            'owner',
            'url',
            "edit_url",
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'public',
        ]


    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('product-edit', kwargs={'pk': obj.pk},request = request)

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-detail", kwargs={"pk": obj.pk},request = request)

