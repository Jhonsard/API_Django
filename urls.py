from django.urls import path, include
from .views import home
from .api.api import product_api_view
from .api.mixing import (
    ProductListCreateView,
    ProductDetailView,
    ProductDetailUpdateView,
    ProductDetailDeleteView) # pour la 4e a la 7e ligne dans path
from .api.mixing import CombinedProductView

app_name = 'api'

urlpatterns = [ 
    path('', home, name='home'),
    path('products/', product_api_view, name='product_api_view'),
    path('products/<int:pk>/', product_api_view, name='product_api_view_data'),
    path('', include('api.api.routers')),
    path('meilleurs2/products/', ProductDetailView.as_view(), name='product_list_create'),
    path('meilleurs2/products/create/', ProductListCreateView.as_view(), name='product_create'),
    path('meilleurs2/products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('meilleurs2/products/<int:pk>/update/', ProductDetailUpdateView.as_view(), name='product_update'),
    path('meilleurs2/products/<int:pk>/delete/', ProductDetailDeleteView.as_view(), name='product_delete'),
    path('combined/products/', CombinedProductView.as_view(), name='combined_product_view'),
    path('combined/products/<int:pk>/', CombinedProductView.as_view(), name='combined_product_detail_view'),
]