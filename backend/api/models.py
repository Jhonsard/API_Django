from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def get_description(self):
        return f"{self.description}"

    def get_price(self):
        return f"{self.price} €" # Exemple de conversion en euros
    
    def get_absolute_url(self):
        return reverse('api:product_api_view_data', args=[str(self.id)]) # Ligne permettant de generer l'url complete du produit

    def __str__(self):
        return self.name