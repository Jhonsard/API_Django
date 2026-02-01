import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product

@csrf_exempt
def home(request):
    if request.method == 'POST':
        post_data = request.body

        # pour convertir le JSON en dictionnaire
        # en enlevant les format bytes b'' des post_data
        data = json.loads(post_data)

        name = data.get('name')
        price = data.get('price')
        description = data.get('description')

        product = Product.objects.create(
            name=name,
            price=price,
            description=description
        )
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
    
    products = Product.objects.all()

    data = [{
        'id': product.id, 'name': product.name, 'price': product.price} for product in products]
    return JsonResponse(data, safe=False)