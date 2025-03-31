from django.http import Http404
from rest_framework import generics, status, mixins, permissions, authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsStaffEditorPermission
from api.authentication import TokenAuthentication as MyTokenAuthentication


class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = self.kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "cool stuff done by mixin view"

        serializer.save(content=content)



class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAdminUser,IsStaffEditorPermission)

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title

        serializer.save(content=content)

# another way of defining view
product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAdminUser,IsStaffEditorPermission)

    # lookup_field = 'pk'

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAdminUser,IsStaffEditorPermission)

    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            # instance.save()

class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAdminUser,IsStaffEditorPermission)

    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class ProductListAPIView(generics.ListAPIView):
    """
    Just to show as a possibility. Real endpoint combined in ProductListCreateAPIView
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['GET', "POST"])
def product_alt_view(request, pk=None ,*args, **kwargs):
    method = request.method

    if method == "GET":
        pass
        if pk is not None:
            # detail view
            # 1 approach
            # queryset = Product.objects.filter(pk=pk)
            # if not queryset.exists():
            #     raise Http404
            # serializer = ProductSerializer(queryset, many=True)
            # return Response(serializer.data)
            # 2 approach
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj).data
            return Response(data)
        else:
            # list view
            queryset = Product.objects.all()
            data = ProductSerializer(queryset, many=True).data
            return Response(data)

    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            print(instance)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)