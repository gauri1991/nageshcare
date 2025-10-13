from django.contrib import admin
from .models import (
    SiteSettings, HeroSection, FeatureCard, TrustIndicator,
    Testimonial, ClientIndustry, CompanyStat, TextContent,
    CallToAction, MediaFile
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Business Information', {
            'fields': ('business_name', 'tagline')
        }),
        ('Contact Information', {
            'fields': ('phone_primary', 'phone_whatsapp', 'email_primary', 'email_support')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'pincode')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url', 'whatsapp_url')
        }),
        ('Business Details', {
            'fields': ('business_hours', 'gst_number', 'cin_number', 'msme_number', 'established_year')
        }),
        ('SEO Defaults', {
            'fields': ('default_meta_description', 'default_meta_keywords')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'title', 'is_active', 'updated_at']
    list_filter = ['page_name', 'is_active']
    search_fields = ['title', 'subtitle', 'description']
    fieldsets = (
        (None, {
            'fields': ('page_name', 'is_active')
        }),
        ('Content', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('CTA Buttons', {
            'fields': ('button1_text', 'button1_url', 'button2_text', 'button2_url')
        }),
        ('Background', {
            'fields': ('background_image',)
        }),
    )


@admin.register(FeatureCard)
class FeatureCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'section_identifier', 'order', 'is_active']
    list_filter = ['section_identifier', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['section_identifier', 'order']


@admin.register(TrustIndicator)
class TrustIndicatorAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'order', 'is_active']
    list_filter = ['position', 'is_active']
    search_fields = ['title', 'subtitle']
    list_editable = ['order', 'is_active']
    ordering = ['position', 'order']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_location', 'rating', 'is_featured', 'is_active', 'order']
    list_filter = ['rating', 'is_featured', 'is_active']
    search_fields = ['customer_name', 'customer_location', 'testimonial_text']
    list_editable = ['is_featured', 'is_active', 'order']
    ordering = ['-is_featured', 'order']


@admin.register(ClientIndustry)
class ClientIndustryAdmin(admin.ModelAdmin):
    list_display = ['industry_name', 'icon_class', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['industry_name', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(CompanyStat)
class CompanyStatAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'section', 'order', 'is_active']
    list_filter = ['section', 'is_active']
    search_fields = ['label', 'value']
    list_editable = ['order', 'is_active']
    ordering = ['section', 'order']


@admin.register(TextContent)
class TextContentAdmin(admin.ModelAdmin):
    list_display = ['content_key', 'page_name', 'section_identifier', 'is_active']
    list_filter = ['page_name', 'is_active']
    search_fields = ['content_key', 'title', 'content']
    prepopulated_fields = {'content_key': ('section_identifier',)}


@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'title', 'is_active']
    list_filter = ['page_name', 'is_active']
    search_fields = ['title', 'description']


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_type', 'uploaded_by', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['title', 'alt_text']
    readonly_fields = ['uploaded_at']

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
