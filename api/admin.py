from django.contrib import admin
from django.utils.html import format_html

# Attempt to use Unfold's admin classes for deeper integration.
try:
    from unfold.admin import ModelAdmin, TabularInline, StackedInline
except ImportError:
    from django.contrib.admin import ModelAdmin, TabularInline, StackedInline # Fallback to Django's standard

from .models import Product, ProductImage, Review


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_preview_inline', 'alt_text', 'caption', 'is_featured')
    readonly_fields = ('image_preview_inline',)
    ordering = ('uploaded_at',)

    def image_preview_inline(self, obj):
        if obj.pk and obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px; object-fit: cover;" />', obj.image.url)
        return "(No image or not saved)"
    image_preview_inline.short_description = 'Preview'


class ReviewInline(TabularInline): # Or StackedInline for more space per review
    model = Review
    extra = 0 # Don't show empty forms for reviews by default
    fields = ('user_name', 'rating', 'comment', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    # classes = ['collapse'] # If you want them collapsible


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'category', 'price', 'sku', 'availability', 'is_featured', 'main_image_thumbnail', 'updated_at')
    list_filter = ('is_featured', 'category', 'availability', 'created_at', 'updated_at', 'price')
    search_fields = ('name', 'description', 'sku', 'category', 'materials')
    readonly_fields = ('created_at', 'updated_at', 'main_image_display')
    inlines = [ProductImageInline, ReviewInline]
    list_per_page = 20
    ordering = ('-updated_at',)

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'price', 'is_featured')
        }),
        ('Inventory & Availability', {
            'fields': ('sku', 'availability')
        }),
        ('Product Details', {
            'fields': ('materials', 'dimensions', 'care_instructions'),
            'classes': ('collapse',), # Optional: make this section collapsible
        }),
        ('Main Image', {
            'fields': ('main_image', 'main_image_display')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def main_image_thumbnail(self, obj):
        if obj.main_image and hasattr(obj.main_image, 'url'):
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover;" />', obj.main_image.url)
        return "No image"
    main_image_thumbnail.short_description = 'Image'

    def main_image_display(self, obj):
        if obj.main_image and hasattr(obj.main_image, 'url'):
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px; object-fit: contain;" />', obj.main_image.url)
        return "No image"
    main_image_display.short_description = 'Current Main Image'


@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    list_display = ('product_link', 'alt_text', 'image_thumbnail_list', 'caption', 'is_featured', 'uploaded_at')
    list_filter = ('product__name', 'is_featured', 'uploaded_at') # Filter by product name
    search_fields = ('alt_text', 'caption', 'product__name')
    readonly_fields = ('image_display',)
    autocomplete_fields = ['product']
    list_per_page = 20
    ordering = ('-uploaded_at',)

    fields = ('product', 'image', 'image_display', 'alt_text', 'caption', 'is_featured')

    def image_thumbnail_list(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover;" />', obj.image.url)
        return "No image"
    image_thumbnail_list.short_description = 'Thumbnail'

    def image_display(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px; object-fit: contain;" />', obj.image.url)
        return "No image"
    image_display.short_description = 'Image Preview'

    def product_link(self, obj):
        from django.urls import reverse
        link = reverse("admin:api_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', link, obj.product.name)
    product_link.short_description = 'Product'
    product_link.admin_order_field = 'product'


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('product_link', 'user_name', 'rating', 'comment_summary', 'created_at')
    list_filter = ('rating', 'created_at', 'product__name') # Filter by product name
    search_fields = ('user_name', 'comment', 'product__name')
    readonly_fields = ('created_at',)
    list_per_page = 20
    ordering = ('-created_at',)

    fields = ('product', 'user_name', 'rating', 'comment', 'created_at')
    autocomplete_fields = ['product'] # For easier product selection

    def comment_summary(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_summary.short_description = 'Comment'

    def product_link(self, obj):
        from django.urls import reverse
        link = reverse("admin:api_product_change", args=[obj.product.id]) # Ensure 'api_product_change' matches your app_label and model_name
        return format_html('<a href="{}">{}</a>', link, obj.product.name)
    product_link.short_description = 'Product'
    product_link.admin_order_field = 'product'