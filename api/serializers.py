from rest_framework import serializers
from .models import Product, ProductImage, Review


class ReviewSerializer(serializers.ModelSerializer):
    # By default, user_name will be included.
    # product field will be the ID.
    class Meta:
        model = Review
        fields = ['id', 'user_name', 'rating', 'comment', 'created_at', 'product']
        read_only_fields = ['created_at', 'product'] # Product ID is usually not changed post-creation of review


class ProductImageSerializer(serializers.ModelSerializer):
    # `image` field will be handled by DRF's FileField/ImageField for uploads if writable,
    # and will provide the URL when reading if configured correctly with MEDIA_URL and context.

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'caption', 'is_featured', 'uploaded_at']
        # 'image' is the actual file field for upload.
        # When reading, DRF's ImageField typically returns the URL to the image.

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.image and hasattr(instance.image, 'url'):
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation


class ProductSerializer(serializers.ModelSerializer):
    gallery_images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True) # Nested reviews

    # main_image is an ImageField in the model, DRF's ModelSerializer will handle it.
    # For uploads, ensure the request is multipart/form-data.
    # When reading, it will provide the URL to the main_image if context is available.

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price',
            'main_image', # This will be the ImageField for upload/URL
            'category', 'sku', 'availability', 'materials',
            'dimensions', 'care_instructions',
            'gallery_images',
            'reviews',
            'is_featured', # Add this field
            'created_at', 'updated_at'
        ]
        # To allow main_image uploads, it should not be in read_only_fields.
        # ModelSerializer handles ImageField for both read (URL) and write (upload).

    def to_representation(self, instance):
        """
        Modify the output representation to ensure full URLs for images.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # Ensure main_image URL is absolute
        if request and instance.main_image and hasattr(instance.main_image, 'url'):
            representation['main_image'] = request.build_absolute_uri(instance.main_image.url)
        elif instance.main_image and not request: # Fallback if no request in context (e.g. management commands)
            representation['main_image'] = instance.main_image.url if hasattr(instance.main_image, 'url') else None


        # The nested ProductImageSerializer's to_representation will handle its own image URLs
        # The nested ReviewSerializer does not have image fields.

        return representation