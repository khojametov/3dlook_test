from django.urls import path
from products.views import (ProductCreateView, ProductDeleteView,
                            ProductDetailView, ProductListView,
                            ProductUpdateView)

urlpatterns = [
    path("list/", ProductListView.as_view(), name="product-list"),
    path("create/", ProductCreateView.as_view(), name="product-create"),
    path("<str:uuid>/", ProductDetailView.as_view(), name="product-detail"),
    path("update/<str:uuid>/", ProductUpdateView.as_view(), name="product-update"),
    path("delete/<str:uuid>/", ProductDeleteView.as_view(), name="product-delete"),
]
