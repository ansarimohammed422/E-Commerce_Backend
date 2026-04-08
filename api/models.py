from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator # For review rating

def product_main_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/products/<product_id>/main/<filename>
    # Note: instance.id might not be available on first save if using a UUID or similar that isn't pre-assigned.
    # For simplicity with standard integer PKs, this often works after the first save or if handled carefully.
    # A more robust solution for new instances might involve signals or saving the image after the instance has an ID.
    product_id_folder = instance.id if instance.id else "temp" # Handle case where ID is not yet set
    return f'products/{product_id_folder}/main/{filename}'

def product_gallery_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/products/<product_id>/gallery/<filename>
    product_id_folder = instance.product.id if instance.product and instance.product.id else "temp"
    return f'products/{product_id_folder}/gallery/{filename}'

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(
        upload_to=product_main_image_path,
        blank=True,
        null=True,
        help_text="Main image for the product."
    )

    # New fields based on frontend mock data
    category = models.CharField(max_length=100, blank=True, null=True, help_text="Product category (e.g., Bags, Wooden Items)")
    sku = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="Stock Keeping Unit")
    availability = models.CharField(max_length=100, blank=True, null=True, help_text="Availability status (e.g., In Stock, Out of Stock)")
    materials = models.TextField(blank=True, null=True, help_text="Materials used for the product")
    dimensions = models.CharField(max_length=255, blank=True, null=True, help_text="Product dimensions")
    care_instructions = models.TextField(blank=True, null=True, help_text="Care instructions for the product")
    is_featured = models.BooleanField(default=False, help_text="Mark as a featured product.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='gallery_images',
        on_delete=models.CASCADE,
        help_text="The product this image belongs to."
    )
    image = models.ImageField(
        upload_to=product_gallery_image_path,
        help_text="Image for the product gallery."
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Descriptive text for the image (for accessibility and SEO)."
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional caption for the image."
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Mark as a featured image in the gallery (if applicable)."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True) # Renamed from created_at for clarity

    class Meta:
        ordering = ['uploaded_at'] # Default ordering for gallery images

    def __str__(self):
        return f"Image for {self.product.name} (ID: {self.id})"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, help_text="The product being reviewed.")
    # In a real system, you'd likely link to a User model:
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100, help_text="Name of the reviewer (or username if anonymous not allowed).")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 (Poor) to 5 (Excellent)."
    )
    comment = models.TextField(help_text="The content of the review.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Show newest reviews first
        # Ensure a user can't review the same product multiple times (if linking to a User model)
        # unique_together = ('product', 'user')

    def __str__(self):
        return f"Review by {self.user_name} for {self.product.name} ({self.rating} stars)"