from api.models import Product
from api.api.serializers import ProductSerializer1, ProductSerializer2
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView

class ProductListCreateView(CreateModelMixin, GenericAPIView): # Liste et Crée des produits
    queryset = Product.objects.all() # Requête pour obtenir tous les produits
    serializer_class = ProductSerializer1 # Sérialiseur pour convertir les objets Produit en JSON et vice versa

    def post(self, request, *args, **kwargs): # POST méthode pour créer un nouveau produit
        return self.create(request, *args, **kwargs) # Appelle la méthode de mixin pour créer un produit
    
class ProductDetailView(RetrieveModelMixin, ListModelMixin, GenericAPIView): # Récupère, Met à jour et Supprime des produits
    queryset = Product.objects.all() # Requête pour obtenir tous les produits
    serializer_class = ProductSerializer2 # Sérialiseur pour convertir les objets Produit en JSON et vice versa

    def get(self, request, *args, **kwargs): # GET méthode pour récupérer un produit spécifique
        if 'pk' not in kwargs:
            return self.list(request, *args, **kwargs) # Si pas de pk, liste tous les produits
        return self.retrieve(request, *args, **kwargs) # Appelle la méthode de mixin pour récupérer le produit
    
    
    
class ProductDetailUpdateView(UpdateModelMixin, GenericAPIView): # Met à jour des produits
    queryset = Product.objects.all() # Requête pour obtenir tous les produits
    serializer_class = ProductSerializer1 # Sérialiseur pour convertir les objets Produit en JSON et vice versa

    def put(self, request, *args, **kwargs): # PUT méthode pour mettre à jour un produit spécifique
        return self.update(request, *args, **kwargs) # Appelle la méthode de mixin pour mettre à jour le produit
    
    def patch(self, request, *args, **kwargs): # PATCH méthode pour mettre à jour partiellement un produit spécifique
        return self.partial_update(request, *args, **kwargs) # Appelle la méthode de mixin pour mettre à jour partiellement le produit
    
class ProductDetailDeleteView(DestroyModelMixin, GenericAPIView): # Supprime des produits
    queryset = Product.objects.all() # Requête pour obtenir tous les produits
    serializer_class = ProductSerializer1 # Sérialiseur pour convertir les objets Produit en JSON et vice versa

    def delete(self, request, *args, **kwargs): # DELETE méthode pour supprimer un produit spécifique
        return self.destroy(request, *args, **kwargs) # Appelle la méthode de mixin pour supprimer le produit
    
class CombinedProductView(
    ProductDetailView,
    ProductListCreateView,
    ProductDetailUpdateView,
    ProductDetailDeleteView,
                            ): # Vue combinée pour gérer les opérations de liste, création, récupération, mise à jour et suppression des produits
    pass
