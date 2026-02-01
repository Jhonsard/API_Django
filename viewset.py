# Implementation of a REST API using Django REST Framework with class-based views (ViewSets)
from api.models import Product
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer1
from rest_framework.decorators import action # pour ajouter un autre route

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer1
    queryset = Product.objects.all()

    # route pour les produits avec un prix sup a 500
    @action(detail=False, methods=['GET'], url_path="expensive-product", url_name="expensive_product")
    def expensive_product(self, request, *args, **kwargs):
        products = Product.objects.filter(price__gte=500)
        context={'request': request}
        serializer = ProductSerializer1(products,many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path="cheap-product", url_name="cheap_product")
    def cheap_product(self, request, *args, **kwargs):
        products = Product.objects.filter(price__lte=12)
        context={'request': request}
        serializer = ProductSerializer1(products,many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)