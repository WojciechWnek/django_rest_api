from rest_framework import viewsets, mixins

from products.models import Product
from products.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    # GET, RETRIEVE, POST, PUT, PATCH, DELETE
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' #default

class ProductGenericViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin):
    # GET, RETRIEVE
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' #defau

# product_list_view = ProductGenericViewSet.as_view({'get': 'list'})
# product_detail_view = ProductGenericViewSet.as_view({'get': 'retrieve'})