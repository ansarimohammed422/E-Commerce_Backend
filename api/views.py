from rest_framework import viewsets
from .models import Product, ProductImage, Review
from .serializers import ProductSerializer, ProductImageSerializer, ReviewSerializer
from .filters import ProductFilter, ReviewFilter, ProductImageFilter # Import filters

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter # Add filterset_class
    # We can add permission_classes later, e.g., [permissions.IsAuthenticatedOrReadOnly]
    # For example, to allow only authenticated users to modify but anyone to read:
    # from rest_framework import permissions
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product gallery images to be viewed or edited.
    """
    queryset = ProductImage.objects.all().order_by('-uploaded_at')
    serializer_class = ProductImageSerializer
    filterset_class = ProductImageFilter # Add filterset_class
    # Add permission_classes as needed, e.g.:
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product reviews.
    """
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilter # Add filterset_class
    # Consider adding permissions, e.g., allow only authenticated users to post.
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Example