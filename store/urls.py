from django.urls import path
from .views import ProductList, ProductDetail

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<str:product_id>/', ProductDetail.as_view()),
]