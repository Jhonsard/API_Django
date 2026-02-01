from django.urls import path
from .views import home
from .api.api import product_api_view

app_name = 'api'

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_api_view, name='product_api_view'),
    path('products/<int:pk>/', product_api_view, name='product_api_view_data'),
]