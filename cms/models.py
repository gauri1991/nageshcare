from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class SiteSettings(models.Model):
    """
    Singleton model for site-wide settings.
    Only one instance should exist.
    """
    # Business Information
    business_name = models.CharField(max_length=200, default='NageshCare')
    tagline = models.CharField(max_length=300, blank=True)

    # Contact Information
    phone_primary = models.CharField(max_length=20)
    phone_whatsapp = models.CharField(max_length=20)
    email_primary = models.EmailField()
    email_support = models.EmailField(blank=True)

    # Address
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True, help_text="Format: https://wa.me/919876543210")

    # Business Details
    business_hours = models.CharField(max_length=200, default='Mon-Sat: 9:00 AM - 6:00 PM')
    gst_number = models.CharField(max_length=20, blank=True)
    cin_number = models.CharField(max_length=30, blank=True)
    msme_number = models.CharField(max_length=30, blank=True)
    established_year = models.CharField(max_length=4, blank=True)

    # SEO Defaults
    default_meta_description = models.TextField(max_length=300, blank=True)
    default_meta_keywords = models.CharField(max_length=500, blank=True)

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return f"{self.business_name} - Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class HeroSection(models.Model):
    """Hero/Banner sections for different pages"""

    PAGE_CHOICES = [
        ('home', 'Home Page'),
        ('about', 'About Page'),
        ('contact', 'Contact Page'),
        ('products', 'Products Page'),
    ]

    ALIGNMENT_CHOICES = [
        ('left', 'Left Aligned'),
        ('center', 'Center Aligned'),
        ('right', 'Right Aligned'),
    ]

    page_name = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    content_alignment = models.CharField(
        max_length=20,
        choices=ALIGNMENT_CHOICES,
        default='left',
        help_text='Text alignment for hero content'
    )

    # CTA Buttons
    button1_text = models.CharField(max_length=100, blank=True)
    button1_url = models.CharField(max_length=200, blank=True)
    button2_text = models.CharField(max_length=100, blank=True)
    button2_url = models.CharField(max_length=200, blank=True)

    # Optional background
    background_image = models.ImageField(upload_to='cms/hero/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Sections'
        ordering = ['page_name']

    def __str__(self):
        return f"Hero - {self.get_page_name_display()}"


class FeatureCard(models.Model):
    """Reusable feature/benefit cards for various sections"""

    SECTION_CHOICES = [
        ('why-choose-us', 'Why Choose Us'),
        ('values', 'Core Values'),
        ('benefits', 'Benefits'),
        ('how-we-work', 'How We Work'),
        ('product-benefits', 'Product Benefits'),
        ('about-vision-mission', 'About - Vision & Mission'),
    ]

    section_identifier = models.CharField(max_length=100, choices=SECTION_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=100,
        help_text='Bootstrap icon class (e.g., bi bi-award-fill)'
    )
    order = models.IntegerField(default=0, help_text='Display order (lower numbers first)')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Feature Card'
        verbose_name_plural = 'Feature Cards'
        ordering = ['section_identifier', 'order', 'id']

    def __str__(self):
        return f"{self.get_section_identifier_display()} - {self.title}"


class TrustIndicator(models.Model):
    """Trust badges and value propositions"""

    POSITION_CHOICES = [
        ('hero', 'Hero Section'),
        ('footer', 'Footer'),
        ('sidebar', 'Sidebar'),
    ]

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    icon_class = models.CharField(
        max_length=100,
        help_text='Bootstrap icon class (e.g., bi bi-gift-fill)'
    )
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='hero')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Trust Indicator'
        verbose_name_plural = 'Trust Indicators'
        ordering = ['position', 'order', 'id']

    def __str__(self):
        return f"{self.title} ({self.get_position_display()})"


class Testimonial(models.Model):
    """Customer testimonials"""

    customer_name = models.CharField(max_length=200)
    customer_role = models.CharField(max_length=200, help_text='e.g., Retail Store Owner')
    customer_location = models.CharField(max_length=200, help_text='e.g., Mumbai')
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    testimonial_text = models.TextField()
    avatar_initials = models.CharField(
        max_length=2,
        help_text='2-letter initials for avatar (e.g., RK)'
    )

    is_featured = models.BooleanField(default=False, help_text='Show on homepage')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['-is_featured', 'order', '-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.customer_location}"


class ClientIndustry(models.Model):
    """Industries served - for 'Trusted By' section"""

    industry_name = models.CharField(max_length=100)
    icon_class = models.CharField(
        max_length=100,
        help_text='Bootstrap icon class (e.g., bi bi-shop)'
    )
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Client Industry'
        verbose_name_plural = 'Client Industries'
        ordering = ['order', 'industry_name']

    def __str__(self):
        return self.industry_name


class CompanyStat(models.Model):
    """Company statistics/metrics (e.g., 100+ Clients, 4.9/5 Rating)"""

    SECTION_CHOICES = [
        ('home-testimonials', 'Home - Testimonials Section'),
        ('footer', 'Footer'),
        ('about', 'About Page'),
    ]

    label = models.CharField(max_length=100, help_text='e.g., Happy Clients')
    value = models.CharField(max_length=50, help_text='e.g., 100+, 4.9/5, 500+')
    icon_class = models.CharField(max_length=100, blank=True)
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, default='home-testimonials')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company Statistic'
        verbose_name_plural = 'Company Statistics'
        ordering = ['section', 'order', 'id']

    def __str__(self):
        return f"{self.value} {self.label}"


class TextContent(models.Model):
    """Generic rich text content blocks for any page/section"""

    PAGE_CHOICES = [
        ('home', 'Home Page'),
        ('about', 'About Page'),
        ('contact', 'Contact Page'),
        ('products', 'Products Page'),
    ]

    page_name = models.CharField(max_length=50, choices=PAGE_CHOICES)
    section_identifier = models.CharField(
        max_length=100,
        help_text='Unique identifier for this content block (e.g., intro-text, company-story)'
    )
    content_key = models.SlugField(
        max_length=100,
        unique=True,
        help_text='Unique key for template usage'
    )
    title = models.CharField(max_length=300, blank=True)
    content = models.TextField(help_text='Rich text content')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Text Content'
        verbose_name_plural = 'Text Content'
        ordering = ['page_name', 'section_identifier']

    def __str__(self):
        return f"{self.get_page_name_display()} - {self.section_identifier}"


class CallToAction(models.Model):
    """CTA sections at page bottoms"""

    PAGE_CHOICES = [
        ('home', 'Home Page'),
        ('about', 'About Page'),
        ('contact', 'Contact Page'),
        ('products', 'Products Page'),
        ('product_detail', 'Product Detail Page'),
    ]

    page_name = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=300)
    description = models.TextField()

    primary_button_text = models.CharField(max_length=100)
    primary_button_url = models.CharField(max_length=200)
    secondary_button_text = models.CharField(max_length=100, blank=True)
    secondary_button_url = models.CharField(max_length=200, blank=True)

    background_color = models.CharField(
        max_length=50,
        default='gradient',
        help_text='CSS class or color'
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Call To Action'
        verbose_name_plural = 'Call To Actions'
        ordering = ['page_name']

    def __str__(self):
        return f"CTA - {self.get_page_name_display()}"


class MediaFile(models.Model):
    """Media library for images and documents"""

    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
    ]

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='cms/media/%Y/%m/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='image')
    alt_text = models.CharField(max_length=200, blank=True)

    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Media File'
        verbose_name_plural = 'Media Files'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    @property
    def is_image(self):
        return self.file_type == 'image'
