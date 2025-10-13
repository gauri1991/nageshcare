from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import os
from datetime import datetime


class Category(models.Model):
    """Product categories - Personal Care, Wellness & Spiritual, etc."""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})


class Product(models.Model):
    """Main product model for wholesale products"""
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tagline = models.CharField(max_length=200, blank=True, help_text="Short catchy tagline")
    short_description = models.TextField(help_text="Brief description for catalog page")
    full_description = models.TextField(help_text="Detailed description for product detail page")

    # Features can be stored as JSON or simple text with line breaks
    features = models.TextField(
        blank=True,
        help_text="Product features, one per line"
    )

    brand_name = models.CharField(max_length=200, blank=True)
    minimum_order_quantity = models.CharField(
        max_length=200,
        blank=True,
        help_text="e.g., '500 packs' or '1,000 sticks'"
    )

    # Status flags
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_coming_soon = models.BooleanField(default=False, help_text="Mark as coming soon")
    is_active = models.BooleanField(default=True)

    # Meta information for SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def get_features_list(self):
        """Return features as a list"""
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []

    def get_primary_image(self):
        """Get the primary product image or first image"""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()


def product_image_upload_path(instance, filename):
    """
    Generate a custom filename for product images
    Format: products/{product-slug}/{product-slug}-{timestamp}-{random}.{ext}
    Example: products/premium-tissue-papers/premium-tissue-papers-20250114-abc123.jpg
    """
    # Get file extension
    ext = filename.split('.')[-1].lower()

    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    # Get product slug (or use ID if slug not available yet)
    product_slug = instance.product.slug if instance.product.slug else f'product-{instance.product.pk}'

    # Generate unique filename
    import uuid
    unique_id = uuid.uuid4().hex[:8]
    new_filename = f'{product_slug}-{timestamp}-{unique_id}.{ext}'

    # Return full path: products/{product-slug}/{filename}
    return os.path.join('products', product_slug, new_filename)


class ProductImage(models.Model):
    """Multiple images for each product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_upload_path)
    is_primary = models.BooleanField(default=False, help_text="Main product image")
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['-is_primary', 'order']

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"

    def save(self, *args, **kwargs):
        # If this is set as primary, unset other primary images for this product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductVariant(models.Model):
    """Different variants of a product (sizes, packaging options, etc.)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    variant_name = models.CharField(
        max_length=200,
        help_text="e.g., 'Pocket Pack (100 sheets)', 'Retail Pack (20 sticks)'"
    )
    description = models.TextField(blank=True)
    specifications = models.TextField(
        blank=True,
        help_text="Technical specifications, one per line"
    )
    order = models.IntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['order', 'variant_name']

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"

    def get_specifications_list(self):
        """Return specifications as a list"""
        if self.specifications:
            return [s.strip() for s in self.specifications.split('\n') if s.strip()]
        return []


class FragranceOption(models.Model):
    """Fragrance options for products like tissue papers and dhoop batti"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='fragrances')
    name = models.CharField(max_length=100, help_text="e.g., 'Lavender Fresh', 'Sandalwood Supreme'")
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g., 'Traditional Sacred', 'Contemporary Wellness'"
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.product.name} - {self.name}"
