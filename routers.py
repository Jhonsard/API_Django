from django.urls import path
from .viewset import ProductViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

"""API Router Configuration
    default routeur est utilise pour les operation CRUD (genere tout les urls)
    simple routeur est utilise pour les operations en lecture seule (genere que les urls pour GET)
"""

# Utilison le defaults router pour les operations CRUD
router = DefaultRouter()
router.register(r'meilleurs/products', ProductViewSet, basename='products')

urlpatterns = router.urls # On utilise les urls generees par le routeur
