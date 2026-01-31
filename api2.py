from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.api.serializers import ProductSerializer1, ProductSerializer2

# comment developper une api rest avec api view ou le decorateur api_view
@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def product_api_view(request, pk=None, *args, **kwargs): # pk est une variable optionnelle ou dynamique
    # Processus de serialisation
    if request.method == 'GET':
        if pk is not None:
            # Recuperation d'un seul element
            product = Product.objects.get(pk=pk) #recuperation de l'instance une seule donnee
            serializer = ProductSerializer1(product) # instance unique
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Recuperation de tous les elements
        products = Product.objects.all() # recuperation de toutes les instances ou donnees
        serializer = ProductSerializer2(products, many=True) # pour signaler qu'on resoit beaucoup d'objets
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Processus de deserialisation
    if request.method == 'POST':
        serializer = ProductSerializer1(data=request.data) # Envoie des donnes au format json
        if serializer.is_valid(raise_exception=True): # lever une exception si les donnes ne sont pas compatibles
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        if pk is None:
            return Response({'detail': 'Method PUT not allowe'}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer1(product, data=request.data) # recuperation des donnes a modifier de l'instance product
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        if pk is None:
            return Response({'detail': 'Method DELETE not allowe'}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'detail': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'PATCH':
        if pk is None:
            return Response({'detail': 'Method PATCH not allowe'}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer1(product, data=request.data, partial=True) # partial pour la mise a jour partielle
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)