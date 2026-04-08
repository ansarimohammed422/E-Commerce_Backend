import django_filters
from .models import Product, Review, ProductImage

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    materials = django_filters.CharFilter(lookup_expr='icontains') # If materials is a TextField

    class Meta:
        model = Product
        fields = {
            'category': ['exact', 'icontains'],
            'availability': ['exact', 'icontains'],
            'sku': ['exact', 'icontains'],
            # Add other fields if direct filtering is needed without specific lookup_expr
            # e.g., 'dimensions': ['exact', 'icontains'],
        }
        # The fields dictionary allows specifying multiple lookup expressions per field.
        # The list version in the description implied only exact matches for some.
        # This explicit dictionary is more flexible.
        # Combining with declared filters:
        # Explicitly declared filters (name, description, min_price, max_price, materials)
        # will take precedence or be additive to what's in Meta fields.

class ReviewFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name="rating", lookup_expr='lte')
    user_name = django_filters.CharFilter(lookup_expr='icontains')
    comment = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Review
        fields = ['product', 'rating', 'user_name', 'comment'] # product allows filtering by product ID

class ProductImageFilter(django_filters.FilterSet):
    class Meta:
        model = ProductImage
        fields = ['product', 'is_featured', 'alt_text', 'caption']
        # product allows filtering by product ID
        # is_featured for boolean filtering
        # alt_text and caption can be filtered with default (exact, icontains if CharField/TextField)
        # Or define them explicitly like in ProductFilter for specific lookups:
        # fields = {
        #     'product': ['exact'],
        #     'is_featured': ['exact'],
        #     'alt_text': ['icontains'],
        #     'caption': ['icontains'],
        # }