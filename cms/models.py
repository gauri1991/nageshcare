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

    # Email Configuration (for replying to inquiries)
    email_host = models.CharField(max_length=200, blank=True, default='smtp.gmail.com', help_text='SMTP server (e.g., smtp.gmail.com)')
    email_port = models.IntegerField(default=587, help_text='SMTP port (587 for TLS, 465 for SSL)')
    email_use_tls = models.BooleanField(default=True, help_text='Use TLS encryption')
    email_host_user = models.EmailField(blank=True, help_text='SMTP username/email')
    email_host_password = models.CharField(max_length=200, blank=True, help_text='SMTP password or app password')
    email_reply_signature = models.TextField(blank=True, default='Best regards,\nNageshCare Team\nwww.nageshcare.com', help_text='Email signature for replies')

    # WhatsApp Floating Button Settings
    whatsapp_float_enabled = models.BooleanField(default=True, help_text='Enable floating WhatsApp button')
    whatsapp_float_message = models.TextField(
        default="Hi, I'm interested in your wholesale products. Please share more details.",
        help_text='Default message text for WhatsApp chat'
    )
    whatsapp_float_position_bottom = models.IntegerField(default=100, help_text='Bottom position in pixels')
    whatsapp_float_position_right = models.IntegerField(default=20, help_text='Right position in pixels')
    whatsapp_float_show_on_mobile = models.BooleanField(default=False, help_text='Show on mobile devices')
    whatsapp_float_show_on_desktop = models.BooleanField(default=True, help_text='Show on desktop/tablet')

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
        ('request-quote', 'Request Quote Page'),
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

    # Additional metric fields for request-quote page (Metric 3)
    metric3_value = models.CharField(max_length=50, blank=True, help_text='Third metric value (e.g., "Zero")')
    metric3_label = models.CharField(max_length=100, blank=True, help_text='Third metric label (e.g., "Obligation")')
    metric3_icon = models.CharField(max_length=100, blank=True, help_text='Bootstrap icon class for third metric')

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
        ('quote-inclusions', 'Request Quote - Quote Inclusions'),
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
        ('request-quote', 'Request Quote Page'),
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
        ('request-quote', 'Request Quote Page'),
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


class ThemeSettings(models.Model):
    """
    Singleton model for theme customization.
    Stores color palettes and typography settings.
    Only one instance should exist.
    """

    PALETTE_CHOICES = [
        ('default', 'Default (Teal & Golden)'),
        ('nature', 'Nature (Forest Green & Cream)'),
        ('professional', 'Professional (Dark & Blue-Gray)'),
        ('custom', 'Custom'),
    ]

    # Active Palette
    active_palette = models.CharField(
        max_length=20,
        choices=PALETTE_CHOICES,
        default='default',
        help_text='Select a pre-configured palette or customize your own'
    )

    # Primary Color Palette
    primary_color = models.CharField(max_length=7, default='#264653', help_text='Primary brand color (e.g., #264653)')
    primary_hover = models.CharField(max_length=7, default='#1A4D59', help_text='Primary hover state')

    # Secondary Color Palette
    secondary_color = models.CharField(max_length=7, default='#E9C46A', help_text='Secondary/accent color (e.g., #E9C46A)')
    secondary_hover = models.CharField(max_length=7, default='#D4AF37', help_text='Secondary hover state')

    # Accent/Tertiary Color
    accent_color = models.CharField(max_length=7, default='#2A9D8F', help_text='Accent color for badges, highlights')

    # Background Colors
    background_light = models.CharField(max_length=7, default='#F8F9FA', help_text='Light background (sections)')
    background_dark = models.CharField(max_length=7, default='#1A3540', help_text='Dark background (footer)')

    # Text Colors
    text_primary = models.CharField(max_length=7, default='#333333', help_text='Main body text color')
    text_secondary = models.CharField(max_length=7, default='#6C757D', help_text='Muted/secondary text')

    # Border Colors
    border_light = models.CharField(max_length=7, default='#F0F0F0', help_text='Light borders')
    border_medium = models.CharField(max_length=7, default='#CED4DA', help_text='Medium borders')

    # Header Colors - Top Bar
    topbar_bg = models.CharField(max_length=7, default='#264653', help_text='Top info bar background')
    topbar_text = models.CharField(max_length=7, default='#FFFFFF', help_text='Top bar text color')
    topbar_link = models.CharField(max_length=7, default='#FFFFFF', help_text='Top bar link color')
    topbar_link_hover = models.CharField(max_length=7, default='#E9C46A', help_text='Top bar link hover')

    # Header Colors - Navigation Bar
    navbar_bg = models.CharField(max_length=7, default='#FFFFFF', help_text='Main navigation background')
    navbar_link = models.CharField(max_length=7, default='#333333', help_text='Navigation link color')
    navbar_link_hover = models.CharField(max_length=7, default='#264653', help_text='Nav link hover color')
    navbar_link_active = models.CharField(max_length=7, default='#264653', help_text='Active nav link color')

    # Section & Content Colors
    section_subtitle = models.CharField(max_length=7, default='#2A9D8F', help_text='Section subtitle/eyebrow text')
    text_muted = models.CharField(max_length=7, default='#6C757D', help_text='Muted/helper text')

    # Icon Colors
    icon_default = models.CharField(max_length=7, default='#264653', help_text='Default icon color')
    icon_hover = models.CharField(max_length=7, default='#2A9D8F', help_text='Icon hover state')
    icon_feature = models.CharField(max_length=7, default='#264653', help_text='Feature card icons')
    icon_trust = models.CharField(max_length=7, default='#E9C46A', help_text='Trust indicator icons')

    # Footer Specific Colors
    footer_bg = models.CharField(max_length=7, default='#1A3540', help_text='Footer background')
    footer_heading = models.CharField(max_length=7, default='#E9C46A', help_text='Footer section headings')
    footer_text = models.CharField(max_length=7, default='#B8C5CC', help_text='Footer body text')
    footer_link = models.CharField(max_length=7, default='#B8C5CC', help_text='Footer links')
    footer_link_hover = models.CharField(max_length=7, default='#E9C46A', help_text='Footer link hover')
    footer_icon = models.CharField(max_length=7, default='#E9C46A', help_text='Footer icons (non-social)')

    # Typography - Headings
    font_heading = models.CharField(
        max_length=100,
        default='Inter',
        help_text='Font family for headings (h1-h6)'
    )
    font_heading_weight = models.IntegerField(default=700, help_text='Font weight for headings')

    # Typography - Body
    font_body = models.CharField(
        max_length=100,
        default='Roboto',
        help_text='Font family for body text'
    )
    font_body_weight = models.IntegerField(default=400, help_text='Font weight for body text')

    # Font Sizes
    font_size_base = models.CharField(max_length=10, default='16px', help_text='Base font size')
    font_size_h1 = models.CharField(max_length=10, default='2.5rem', help_text='H1 size')
    font_size_h2 = models.CharField(max_length=10, default='2rem', help_text='H2 size')
    font_size_h3 = models.CharField(max_length=10, default='1.75rem', help_text='H3 size')
    font_size_h4 = models.CharField(max_length=10, default='1.5rem', help_text='H4 size')
    font_size_h5 = models.CharField(max_length=10, default='1.25rem', help_text='H5 size')
    font_size_h6 = models.CharField(max_length=10, default='1rem', help_text='H6 size')

    # Spacing & Shadows
    border_radius = models.CharField(max_length=10, default='8px', help_text='Default border radius')
    box_shadow_default = models.CharField(max_length=100, default='0 4px 6px rgba(0, 0, 0, 0.08)', help_text='Default box shadow')
    box_shadow_hover = models.CharField(max_length=100, default='0 8px 15px rgba(0, 0, 0, 0.15)', help_text='Hover box shadow')

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Theme Settings'
        verbose_name_plural = 'Theme Settings'

    def __str__(self):
        return f"Theme Settings - {self.get_active_palette_display()}"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion
        pass

    @classmethod
    def load(cls):
        """Load or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def apply_palette(self, palette_name):
        """Apply a pre-configured color palette"""
        palettes = {
            'default': {
                # Core Colors
                'primary_color': '#264653',
                'primary_hover': '#1A4D59',
                'secondary_color': '#E9C46A',
                'secondary_hover': '#D4AF37',
                'accent_color': '#2A9D8F',
                'background_light': '#F8F9FA',
                'background_dark': '#1A3540',
                'text_primary': '#333333',
                'text_secondary': '#6C757D',
                'border_light': '#F0F0F0',
                'border_medium': '#CED4DA',
                # Header - Top Bar
                'topbar_bg': '#264653',
                'topbar_text': '#FFFFFF',
                'topbar_link': '#FFFFFF',
                'topbar_link_hover': '#E9C46A',
                # Header - Navigation
                'navbar_bg': '#FFFFFF',
                'navbar_link': '#333333',
                'navbar_link_hover': '#264653',
                'navbar_link_active': '#264653',
                # Content
                'section_subtitle': '#2A9D8F',
                'text_muted': '#6C757D',
                # Icons
                'icon_default': '#264653',
                'icon_hover': '#2A9D8F',
                'icon_feature': '#264653',
                'icon_trust': '#E9C46A',
                # Footer
                'footer_bg': '#1A3540',
                'footer_heading': '#E9C46A',
                'footer_text': '#B8C5CC',
                'footer_link': '#B8C5CC',
                'footer_link_hover': '#E9C46A',
                'footer_icon': '#E9C46A',
                # Typography
                'font_heading': 'Inter',
                'font_body': 'Roboto',
            },
            'nature': {
                # Core Colors
                'primary_color': '#0A5F45',
                'primary_hover': '#084B36',
                'secondary_color': '#FEECD7',
                'secondary_hover': '#FDD9B0',
                'accent_color': '#2E8B57',
                'background_light': '#FFF9F5',
                'background_dark': '#0A2E23',
                'text_primary': '#2D3A35',
                'text_secondary': '#6B7A73',
                'border_light': '#F5EFE7',
                'border_medium': '#D4C9BD',
                # Header - Top Bar
                'topbar_bg': '#0A5F45',
                'topbar_text': '#FEECD7',
                'topbar_link': '#FEECD7',
                'topbar_link_hover': '#FFFFFF',
                # Header - Navigation
                'navbar_bg': '#FEECD7',
                'navbar_link': '#0A5F45',
                'navbar_link_hover': '#2E8B57',
                'navbar_link_active': '#0A5F45',
                # Content
                'section_subtitle': '#2E8B57',
                'text_muted': '#6B7A73',
                # Icons
                'icon_default': '#0A5F45',
                'icon_hover': '#2E8B57',
                'icon_feature': '#0A5F45',
                'icon_trust': '#FEECD7',
                # Footer
                'footer_bg': '#0A2E23',
                'footer_heading': '#FEECD7',
                'footer_text': '#D4C9BD',
                'footer_link': '#D4C9BD',
                'footer_link_hover': '#FEECD7',
                'footer_icon': '#FEECD7',
                # Typography
                'font_heading': 'DM Sans',
                'font_body': 'Heebo',
            },
            'professional': {
                # Core Colors
                'primary_color': '#19272B',
                'primary_hover': '#0D1517',
                'secondary_color': '#AFC1C5',
                'secondary_hover': '#8FA4AA',
                'accent_color': '#4F595E',
                'background_light': '#F5F7F8',
                'background_dark': '#233036',
                'text_primary': '#19272B',
                'text_secondary': '#4F595E',
                'border_light': '#E5E9EB',
                'border_medium': '#CED5D9',
                # Header - Top Bar
                'topbar_bg': '#19272B',
                'topbar_text': '#AFC1C5',
                'topbar_link': '#AFC1C5',
                'topbar_link_hover': '#FFFFFF',
                # Header - Navigation
                'navbar_bg': '#FFFFFF',
                'navbar_link': '#19272B',
                'navbar_link_hover': '#4F595E',
                'navbar_link_active': '#19272B',
                # Content
                'section_subtitle': '#4F595E',
                'text_muted': '#4F595E',
                # Icons
                'icon_default': '#19272B',
                'icon_hover': '#4F595E',
                'icon_feature': '#19272B',
                'icon_trust': '#AFC1C5',
                # Footer
                'footer_bg': '#233036',
                'footer_heading': '#AFC1C5',
                'footer_text': '#CED5D9',
                'footer_link': '#CED5D9',
                'footer_link_hover': '#AFC1C5',
                'footer_icon': '#AFC1C5',
                # Typography
                'font_heading': 'DM Sans',
                'font_body': 'Heebo',
            },
        }

        if palette_name in palettes:
            palette = palettes[palette_name]
            for key, value in palette.items():
                setattr(self, key, value)
            self.active_palette = palette_name
