from django.db import models
from products.models import Product


class ContactMessage(models.Model):
    """General contact form submissions"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('closed', 'Closed'),
    ]

    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('product_info', 'Product Information'),
        ('bulk_order', 'Bulk Order Quote'),
        ('custom_branding', 'Custom Branding'),
        ('partnership', 'Partnership Opportunity'),
        ('complaint', 'Complaint/Feedback'),
        ('other', 'Other'),
    ]

    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('whatsapp', 'WhatsApp'),
    ]

    # Basic Information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    business_name = models.CharField(max_length=200, blank=True)

    # Inquiry Details
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    product_interest = models.CharField(max_length=200, blank=True)
    message = models.TextField()

    # Contact Preferences
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=CONTACT_METHOD_CHOICES,
        default='email'
    )
    best_time_to_call = models.CharField(max_length=100, blank=True)

    # Status Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    is_read = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin use")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.created_at.strftime('%Y-%m-%d')})"


class Inquiry(models.Model):
    """Product-specific inquiries from product detail pages"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('quoted', 'Quote Sent'),
        ('closed', 'Closed'),
    ]

    # Product Reference
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='inquiries')

    # Basic Information
    name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)

    # Order Details
    quantity_needed = models.CharField(max_length=100, help_text="e.g., '500-1000 packs'")
    preferred_variant = models.CharField(max_length=200, blank=True)
    fragrance_preference = models.CharField(max_length=200, blank=True)

    # Branding & Location
    custom_branding_required = models.BooleanField(default=False)
    delivery_location = models.CharField(max_length=300)

    # Additional Information
    additional_requirements = models.TextField(blank=True)

    # Status Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        product_name = self.product.name if self.product else "Product Deleted"
        return f"{self.name} - {product_name} ({self.created_at.strftime('%Y-%m-%d')})"


class QuoteRequest(models.Model):
    """Detailed bulk order quote requests"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewing', 'Under Review'),
        ('quoted', 'Quote Sent'),
        ('negotiating', 'In Negotiation'),
        ('accepted', 'Quote Accepted'),
        ('rejected', 'Quote Rejected'),
        ('closed', 'Closed'),
    ]

    BUSINESS_TYPE_CHOICES = [
        ('retail_store', 'Retail Store'),
        ('supermarket', 'Supermarket/Chain'),
        ('hotel_resort', 'Hotel/Resort'),
        ('spa_salon', 'Spa/Salon'),
        ('temple_ashram', 'Temple/Ashram'),
        ('yoga_studio', 'Yoga Studio/Wellness Center'),
        ('distributor', 'Distributor/Wholesaler'),
        ('online_seller', 'Online Seller/E-commerce'),
        ('event_planner', 'Event Planner'),
        ('corporate', 'Corporate Office'),
        ('other', 'Other'),
    ]

    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone Call'),
        ('whatsapp', 'WhatsApp'),
        ('any', 'Any of the Above'),
    ]

    ORDER_FREQUENCY_CHOICES = [
        ('one_time', 'One-Time Order'),
        ('monthly', 'Monthly Regular Orders'),
        ('quarterly', 'Quarterly Orders'),
        ('biannual', 'Bi-Annual Orders'),
        ('trial_based', 'Will Decide Based on Trial Order'),
    ]

    # Business Information
    name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=300)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES)
    years_in_business = models.CharField(max_length=50, blank=True)
    business_website = models.URLField(blank=True)
    gst_number = models.CharField(max_length=50, blank=True)

    # Contact Details
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    alternative_contact = models.CharField(max_length=20, blank=True)
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=CONTACT_METHOD_CHOICES,
        default='email'
    )
    best_time_to_reach = models.CharField(max_length=200, blank=True)

    # Product Requirements (stored as text, could be JSON in production)
    product_interests = models.TextField(help_text="Products interested in")
    tissue_variant = models.CharField(max_length=200, blank=True)
    tissue_fragrance = models.CharField(max_length=200, blank=True)
    tissue_quantity = models.CharField(max_length=200, blank=True)
    dhoop_pack_size = models.CharField(max_length=200, blank=True)
    dhoop_fragrance = models.CharField(max_length=200, blank=True)
    dhoop_quantity = models.CharField(max_length=200, blank=True)

    # Order Details
    order_frequency = models.CharField(
        max_length=50,
        choices=ORDER_FREQUENCY_CHOICES,
        blank=True
    )
    timeline = models.CharField(max_length=100, blank=True, help_text="When do they need it?")
    sample_order_first = models.BooleanField(default=False)

    # Customization & Branding
    custom_branding_required = models.BooleanField(default=False)
    brand_name = models.CharField(max_length=200, blank=True)
    has_logo = models.BooleanField(default=False)
    branding_requirements = models.TextField(blank=True)
    logo_file = models.FileField(upload_to='quote_logos/', blank=True, null=True)

    # Delivery & Logistics
    delivery_city = models.CharField(max_length=100)
    delivery_state = models.CharField(max_length=100)
    delivery_pin = models.CharField(max_length=10)
    delivery_address_type = models.CharField(max_length=100, blank=True)
    special_delivery_requirements = models.TextField(blank=True)

    # Budget & Pricing
    budget_range = models.CharField(max_length=100, blank=True)
    payment_terms_preference = models.CharField(max_length=200, blank=True)

    # Additional Information
    how_heard_about_us = models.CharField(max_length=200, blank=True)
    specific_requirements = models.TextField(blank=True)
    wants_call_discussion = models.BooleanField(default=False)

    # Consent & Privacy
    agreed_to_contact = models.BooleanField(default=True)
    wants_updates = models.BooleanField(default=False)

    # Status Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    reference_id = models.CharField(max_length=20, unique=True, blank=True)
    admin_notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quote Request'
        verbose_name_plural = 'Quote Requests'

    def __str__(self):
        return f"{self.business_name} - {self.name} ({self.created_at.strftime('%Y-%m-%d')})"

    def save(self, *args, **kwargs):
        if not self.reference_id:
            # Generate a unique reference ID
            import random
            import string
            self.reference_id = 'QR' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)
