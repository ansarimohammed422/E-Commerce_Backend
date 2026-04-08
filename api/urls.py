from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductImageViewSet, ReviewViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-images', ProductImageViewSet, basename='productimage')
router.register(r'reviews', ReviewViewSet, basename='review')

# The API URLs are now determined automatically by the router.
# This will create URLs like:
# /api/products/
# /api/products/<pk>/
# /api/reviews/
# /api/reviews/<pk>/
urlpatterns = [
    path('', include(router.urls)),
]