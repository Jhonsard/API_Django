from django.http import JsonResponse
from api.models import Product
from rest_framework.response import Response
from django.shortcuts import get_object_or_404 # recuperer un objet ou renvoyer une erreur 404
from rest_framework.decorators import api_view
from rest_framework import status
from api.api.serializers import ProductSerializer1, ProductSerializer2

def get_products(request, pk):
    if pk is not None:
        # Recuperation d'un seul element
        product = get_object_or_404(Product, pk=pk) #recuperation de l'instance une seule donnee
        context = {'request': request} # pour le champ hyperlien defini dans le serializer file
        serializer = ProductSerializer2(product, context=context) # instance unique
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Recuperation de tous les elements
    products = Product.objects.all() # recuperation de toutes les instances ou donnees
    context = {'request': request} # pour le champ hyperlien defini dans le serializer file
    serializer = ProductSerializer1(products, many=True, context=context) # pour signaler qu'on resoit beaucoup d'objets et context pour le champ hyperlien
    return Response(serializer.data, status=status.HTTP_200_OK)

def create_product(request):
    context = {'request': request} # pour le champ hyperlien defini dans le serializer file
    serializer = ProductSerializer1(data=request.data, context=context) # Envoie des donnes au format json
    if serializer.is_valid(raise_exception=True): # lever une exception si les donnes ne sont pas compatibles
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_product(request, pk):
    if pk is None:
        return Response({'detail': 'Method PUT not allowed provide a pk'}, status=status.HTTP_400_BAD_REQUEST)
    product = get_object_or_404(Product, pk=pk)
    context = {'request': request} # pour le champ hyperlien defini dans le serializer file
    serializer = ProductSerializer1(product, data=request.data, context=context) # recuperation des donnes a modifier de l'instance product
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_product(pk):
    if pk is None:
        return Response({'detail': 'Method DELETE not allowed provide a pk'}, status=status.HTTP_400_BAD_REQUEST)
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return Response({'detail': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)

def partial_update_product(request, pk):
    if pk is None:
        return Response({'detail': 'Method PATCH not allowed provide a pk'}, status=status.HTTP_400_BAD_REQUEST)
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer1(product, data=request.data, partial=True) # partial pour la mise a jour partielle
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# comment developper une api rest avec api view ou le decorateur api_view
@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def product_api_view(request, pk=None, *args, **kwargs): # pk est une variable optionnelle ou dynamique
    if request.method == 'GET':
        return get_products(request, pk)
    elif request.method == 'POST':
        return create_product(request)
    elif request.method == 'PUT':
        return update_product(request, pk)
    elif request.method == 'DELETE':
        return delete_product(pk)
    elif request.method == 'PATCH':
        return partial_update_product(request, pk)