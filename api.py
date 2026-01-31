from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.api.serializers import ProductSerializer1, ProductSerializer2

# comment developper une api rest avec api view ou le decorateur api_view
@api_view(['GET', 'POST'])
def product_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer2(products, many=True) # pour signaler qu'on resoit beaucoup d'objets
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Processus de deserialisation
    elif request.method == 'POST':
        serializer = ProductSerializer1(data=request.data) # Envoie des donnes au format json
        if serializer.is_valid(raise_exception=True): # lever une exception si les donnes ne sont pas compatibles
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)