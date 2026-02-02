# Guide de Création d'une API REST avec Django

**Date :** 27/01/2026 - 01/02/2026  
**Auteur :** Documentation du projet APIsProj  

**Note :** Les développeurs travaillent sur les APIs en backend. Les utilisateurs utilisent le frontend ou le client pour consommer les APIs.

---

## Introduction

Ce guide présente les étapes pour créer une API REST en utilisant Django et Django REST Framework (DRF). Il couvre la configuration de l'environnement, la création des modèles, des vues, des sérialiseurs, et l'utilisation des ViewSets pour simplifier le développement.

---

## Étape 1 : Création d'un Environnement Virtuel

- Commande : `python3 -m venv venv`
- Activation : `source venv/bin/activate`

## Étape 2 : Installation des Dépendances

- Créer un fichier `requirements.txt` dans l'environnement virtuel.
- Ajouter les packages nécessaires (ex. : Django, djangorestframework).
- Installation : `pip install -r requirements.txt`

## Étape 3 : Création du Projet Django

- Entrer dans le dossier `backend`.
- Commande : `django-admin startproject core .`

## Étape 4 : Création d'une Application Django

- Toujours dans `backend`.
- Commande : `django-admin startapp nom_de_l_application` (ex. : `api`)
- Conseil : Ouvrir deux terminaux ; un pour le backend, un pour tester le frontend.

## Étape 5 : Configuration des Applications Installées

- Ouvrir `core/settings.py`.
- Dans `INSTALLED_APPS`, ajouter le nom de l'application locale (ex. : `'api'`).

## Étape 6 : Création du Fichier URLs de l'Application

- Dans le dossier `api`, créer un fichier `urls.py`.

## Étape 7 : Implémentation du Fichier URLs

- Importer `path` de `django.urls`.
- Créer une liste vide `urlpatterns`.

```python
# api/urls.py
from django.urls import path

urlpatterns = [
    # À remplir plus tard
]
```

## Étape 8 : Configuration des URLs Principales

- Ouvrir `core/urls.py`.
- Importer `include` de `django.urls`.
- Ajouter dans `urlpatterns` :

```python
path('api/', include('api.urls'))
```

## Étape 9 : Implémentation des Données JSON dans les Vues

- Ouvrir `api/views.py`.
- Importer `JsonResponse` de `django.http`.
- Définir une fonction `home` :

```python
def home(request):
    return JsonResponse({"message": "Hello World"})
```

## Étape 10 : Liaison des URLs et Test

- Dans `api/urls.py`, importer `home` et ajouter :

```python
path('', home, name='home')
```

- Pour tester : Créer un fichier `test.py` dans `client`.
- Importer `requests`.
- Définir l'endpoint : `endpoint = "http://localhost:8000/api"`
- Démarrer le serveur : `python3 manage.py runserver`
- Tester avec `requests.get(endpoint)`

**Note :** Pour passer des paramètres GET, ajouter `?q=valeur` à l'URL. Récupérer avec `request.GET.get('q')`.

---

## Étape 11 : Création du Modèle de Données

- Ouvrir `api/models.py`.
- Créer une classe `Product` héritant de `models.Model` :

```python
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
```

- Migrations : `python3 manage.py makemigrations` puis `python3 manage.py migrate`.

---

## Étape 12 : Gestion des Requêtes POST

- Créer un fichier `create_product.py` dans `client`.
- Importer `requests`.
- Définir les données et envoyer :

```python
data = {"name": "Produit", "price": 10.00, "description": "Desc"}
response = requests.post(endpoint, json=data)
```

- Dans `views.py`, gérer le POST :

```python
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        product = Product.objects.create(**data)
        return JsonResponse({"id": product.id, "name": product.name})
    # Logique GET
```

**Note :** `@csrf_exempt` désactive la vérification CSRF pour les APIs publiques.

---

## Étape 13 : Intégration du Modèle dans les Vues

- Importer `Product` dans `views.py`.
- Pour GET : Retourner la liste des produits.
- Pour POST : Créer et retourner le produit.

---

## Étape 14 : Introduction à Django REST Framework (DRF)

- Ajouter `'rest_framework'` dans `INSTALLED_APPS` de `settings.py`.
- Créer un sous-dossier `api` dans `api/`, avec `api.py` et `serializers.py`.
- Dans `serializers.py` :

```python
from rest_framework import serializers
from api.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

- Dans `api.py` :

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from api.models import Product

@api_view(['GET', 'POST'])
def product_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    # Logique POST
```

---

## Étape 15 : Ajout des Méthodes PUT et DELETE

- Utiliser `get_object_or_404` pour récupérer un objet.
- Ajouter `'PUT'`, `'DELETE'` dans `@api_view`.
- Exemple pour GET d'un élément :

```python
if request.method == 'GET':
    if pk:
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
```

---

## Étape 16 : Utilisation de Thunder Client pour les Tests
- Installer l'extension Thunder Client dans VS Code.
- Créer une nouvelle requête, sélectionner la méthode (GET, POST, etc.).
- Entrer l'endpoint et cliquer sur "Send".
- Avantage : Évite de créer des fichiers de test manuels.

---

## Étape 17 : Validation des Données
- **Au niveau de l'API :**
  ```python
  if request.method == 'POST':
      name = request.data.get('name')
      if name in ['donald', 'trump']:
          return Response({"error": "Nom non autorisé"})
  ```
- **Au niveau du Serializer :**
  ```python
  class ProductSerializer(serializers.ModelSerializer):
      def validate_name(self, value):
          if value.lower() in ['donald', 'trump']:
              raise serializers.ValidationError("Nom non autorisé")
          return value
  ```

---

## Étape 18 : Utilisation des ViewSets
- Créer un fichier `routers.py` ou intégrer dans `urls.py`.
- Exemple :
  ```python
  from rest_framework.routers import DefaultRouter
  from .api.api import ProductViewSet

  router = DefaultRouter()
  router.register(r'products', ProductViewSet)
  urlpatterns = router.urls
  ```
- Dans `api.py` :
  ```python
  from rest_framework.viewsets import ModelViewSet

  class ProductViewSet(ModelViewSet):
      queryset = Product.objects.all()
      serializer_class = ProductSerializer
  ```
### Étape 19 : Configuration personnalisée d'un formulaire d'entrée des données
- Aller dans `settings.py` du package `core`.
- Au-dessus de la liste `MIDDLEWARE`, déclarer :

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',  # Accepte des données au format JSON
        'rest_framework.parsers.FormParser',  # Accepte des données au format form-data
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}
```

- Importer `action` depuis `rest_framework.decorators`.
- Implémenter les actions personnalisées dans le ViewSet :

```python
# Route pour les produits avec un prix supérieur ou égal à 500 €
@action(detail=False, methods=['GET'], url_path="expensive-product", url_name="expensive_product")
def expensive_product(self, request, *args, **kwargs):
    products = Product.objects.filter(price__gte=500)
    context = {'request': request}
    serializer = ProductSerializer1(products, many=True, context=context)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Route pour les produits avec un prix inférieur ou égal à 12 €
@action(detail=False, methods=['GET'], url_path="cheap-product", url_name="cheap_product")
def cheap_product(self, request, *args, **kwargs):
    products = Product.objects.filter(price__lte=12)
    context = {'request': request}
    serializer = ProductSerializer1(products, many=True, context=context)
    return Response(serializer.data, status=status.HTTP_200_OK)
```

- Ces routes seront accessibles via :
  - Produits chers : `http://localhost:8000/api/meilleurs/products/expensive-product/`
  - Produits bon marché : `http://localhost:8000/api/meilleurs/products/cheap-product/`

### Étape 20 : Création d'un fichier `mixing.py`

- Créer un fichier `mixing.py` dans le répertoire `api`.
- Importer les classes nécessaires :

```python
from .models import Product
from .serializers import ProductSerializer1
from rest_framework.mixins import *
from rest_framework.generics import GenericAPIView
```

- Implémenter les vues avec mixins :

```python
class ProductListCreateView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer1

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer1

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ProductDetailUpdateView(UpdateModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer1

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class ProductDetailDeleteView(DestroyModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer1

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

- Ajouter les chemins dans `urls.py` du projet :

```python
from .mixing import ProductListCreateView, ProductDetailView, ProductDetailUpdateView, ProductDetailDeleteView

urlpatterns = [
    # ... autres chemins ...
    path('meilleurs2/products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('meilleurs2/products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('meilleurs2/products/<int:pk>/update/', ProductDetailUpdateView.as_view(), name='product_update'),
    path('meilleurs2/products/<int:pk>/delete/', ProductDetailDeleteView.as_view(), name='product_delete'),
]
```

- Pour simplifier, créer une vue combinée :

```python
class CombinedProductView(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer1

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

- Ajouter le chemin pour la vue combinée :

```python
path('combined/products/', CombinedProductView.as_view(), name='combined_product_view'),
path('combined/products/<int:pk>/', CombinedProductView.as_view(), name='combined_product_detail_view'),
```

- Accès via :
  - Liste et création : `http://localhost:8000/api/combined/products/`
  - Détail, mise à jour, suppression : `http://localhost:8000/api/combined/products/<id>/`

---

**Conseils Généraux :**
- Toujours activer l'environnement virtuel avant de travailler.
- Tester régulièrement l'API avec le serveur en cours d'exécution.
- Utiliser Django REST Framework pour simplifier la sérialisation et la validation des données.
- Éviter d'ajouter des champs dans le sérialiseur qui n'existent pas dans le modèle, sauf en cas de surcharge de la méthode `create`.
- Le `ReadOnlyModelViewSet` dans `views.py` permet uniquement les opérations GET (lecture seule).
- Documenter les endpoints personnalisés pour faciliter la maintenance.

Cette documentation couvre les bases de la création d'une API REST avec Django et Django REST Framework.
