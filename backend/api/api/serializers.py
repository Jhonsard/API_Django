from api.models import Product
from rest_framework import serializers

# Serialiseur qui n'envoie pas trop de champs
# Peut être utile pour la méthode post
class ProductSerializer1(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    description_euros = serializers.SerializerMethodField(read_only=True)  # champ en lecture seule
    
    # Champ de lien hypertexte vers l'objet détail
    link = serializers.HyperlinkedIdentityField(
        view_name='api:product_api_view_data',
        lookup_field='pk'
    )
    

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description_euros', 'link']
        read_only_fields = ['create_at', 'update_at']

    def get_description_euros(self, obj):
        return f"{obj.get_description()} - {obj.get_price()}"

    def validate_name(self, value):
        if value.lower() in ["donald", "trump", "donald trump"]:
            raise serializers.ValidationError("Vous n'êtes pas autorisé d'utiliser ce nom")
        return value
        
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
        
# Serialiseur qui ne renvoie seulement que trois champs
# Peut être utile pour la méthode get.
# Nous ne pouvons pas y faire une création automatique, on oblige le modèle
class ProductSerializer2(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    # La méthode de surcharge, 
    def create(self, validated_data):
        return Product.objects.create(**validated_data)  # retourne un objet différent ici
