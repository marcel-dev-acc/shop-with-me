from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllProducts.as_view(), name="products"),
    path('<int:product_id>/', views.ProductDetail.as_view(), name='product_detail'),
]
