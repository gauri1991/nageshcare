from django.contrib import admin
from .models import ContactMessage, Inquiry, QuoteRequest


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'is_read', 'created_at']
    list_filter = ['status', 'is_read', 'subject', 'created_at']
    search_fields = ['name', 'email', 'phone', 'business_name', 'message']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'business_name')
        }),
        ('Inquiry Details', {
            'fields': ('subject', 'product_interest', 'message')
        }),
        ('Contact Preferences', {
            'fields': ('preferred_contact_method', 'best_time_to_call')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'is_read', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_contacted', 'mark_as_closed']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} messages marked as read.')
    mark_as_read.short_description = 'Mark selected as read'

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f'{queryset.count()} messages marked as unread.')
    mark_as_unread.short_description = 'Mark selected as unread'

    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')
        self.message_user(request, f'{queryset.count()} messages marked as contacted.')
    mark_as_contacted.short_description = 'Mark as contacted'

    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
        self.message_user(request, f'{queryset.count()} messages marked as closed.')
    mark_as_closed.short_description = 'Mark as closed'


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'business_name', 'product', 'quantity_needed', 'custom_branding_required', 'status', 'created_at']
    list_filter = ['status', 'custom_branding_required', 'product', 'created_at']
    search_fields = ['name', 'business_name', 'email', 'phone', 'delivery_location']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'business_name', 'email', 'phone', 'whatsapp_number')
        }),
        ('Product Details', {
            'fields': ('product', 'quantity_needed', 'preferred_variant', 'fragrance_preference')
        }),
        ('Branding & Delivery', {
            'fields': ('custom_branding_required', 'delivery_location')
        }),
        ('Additional Information', {
            'fields': ('additional_requirements',)
        }),
        ('Status & Tracking', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_contacted', 'mark_as_quoted', 'mark_as_closed']

    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')
        self.message_user(request, f'{queryset.count()} inquiries marked as contacted.')
    mark_as_contacted.short_description = 'Mark as contacted'

    def mark_as_quoted(self, request, queryset):
        queryset.update(status='quoted')
        self.message_user(request, f'{queryset.count()} inquiries marked as quoted.')
    mark_as_quoted.short_description = 'Mark as quote sent'

    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
        self.message_user(request, f'{queryset.count()} inquiries marked as closed.')
    mark_as_closed.short_description = 'Mark as closed'


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['reference_id', 'business_name', 'name', 'business_type', 'status', 'created_at']
    list_filter = ['status', 'business_type', 'custom_branding_required', 'sample_order_first', 'created_at']
    search_fields = ['reference_id', 'name', 'business_name', 'email', 'phone', 'delivery_city', 'gst_number']
    readonly_fields = ['reference_id', 'created_at', 'updated_at']
    list_editable = ['status']

    fieldsets = (
        ('Reference', {
            'fields': ('reference_id',)
        }),
        ('Business Information', {
            'fields': ('name', 'business_name', 'business_type', 'years_in_business', 'business_website', 'gst_number')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'whatsapp_number', 'alternative_contact', 'preferred_contact_method', 'best_time_to_reach')
        }),
        ('Product Requirements', {
            'fields': ('product_interests', 'tissue_variant', 'tissue_fragrance', 'tissue_quantity',
                      'dhoop_pack_size', 'dhoop_fragrance', 'dhoop_quantity'),
            'classes': ('collapse',)
        }),
        ('Order Details', {
            'fields': ('order_frequency', 'timeline', 'sample_order_first')
        }),
        ('Customization & Branding', {
            'fields': ('custom_branding_required', 'brand_name', 'has_logo', 'branding_requirements', 'logo_file'),
            'classes': ('collapse',)
        }),
        ('Delivery & Logistics', {
            'fields': ('delivery_city', 'delivery_state', 'delivery_pin', 'delivery_address_type', 'special_delivery_requirements')
        }),
        ('Budget & Pricing', {
            'fields': ('budget_range', 'payment_terms_preference'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('how_heard_about_us', 'specific_requirements', 'wants_call_discussion'),
            'classes': ('collapse',)
        }),
        ('Consent', {
            'fields': ('agreed_to_contact', 'wants_updates'),
            'classes': ('collapse',)
        }),
        ('Status & Tracking', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_reviewing', 'mark_as_quoted', 'mark_as_negotiating', 'mark_as_accepted', 'mark_as_rejected', 'mark_as_closed']

    def mark_as_reviewing(self, request, queryset):
        queryset.update(status='reviewing')
        self.message_user(request, f'{queryset.count()} quote requests marked as under review.')
    mark_as_reviewing.short_description = 'Mark as under review'

    def mark_as_quoted(self, request, queryset):
        queryset.update(status='quoted')
        self.message_user(request, f'{queryset.count()} quote requests marked as quoted.')
    mark_as_quoted.short_description = 'Mark as quote sent'

    def mark_as_negotiating(self, request, queryset):
        queryset.update(status='negotiating')
        self.message_user(request, f'{queryset.count()} quote requests marked as in negotiation.')
    mark_as_negotiating.short_description = 'Mark as in negotiation'

    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')
        self.message_user(request, f'{queryset.count()} quote requests marked as accepted.')
    mark_as_accepted.short_description = 'Mark as accepted'

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} quote requests marked as rejected.')
    mark_as_rejected.short_description = 'Mark as rejected'

    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
        self.message_user(request, f'{queryset.count()} quote requests marked as closed.')
    mark_as_closed.short_description = 'Mark as closed'
