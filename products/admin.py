from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, FragranceOption


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary', 'alt_text', 'order']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['variant_name', 'description', 'specifications', 'order']


class FragranceOptionInline(admin.TabularInline):
    model = FragranceOption
    extra = 1
    fields = ['name', 'description', 'category', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_featured', 'is_coming_soon', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_coming_soon', 'is_active', 'created_at']
    search_fields = ['name', 'short_description', 'full_description', 'tagline']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductImageInline, ProductVariantInline, FragranceOptionInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'tagline', 'brand_name')
        }),
        ('Description', {
            'fields': ('short_description', 'full_description', 'features')
        }),
        ('Order Information', {
            'fields': ('minimum_order_quantity',)
        }),
        ('Status & Visibility', {
            'fields': ('is_featured', 'is_coming_soon', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_featured', 'mark_as_not_featured', 'mark_as_active', 'mark_as_inactive']

    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} products marked as featured.')
    mark_as_featured.short_description = 'Mark selected products as featured'

    def mark_as_not_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} products unmarked as featured.')
    mark_as_not_featured.short_description = 'Unmark selected products as featured'

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} products marked as active.')
    mark_as_active.short_description = 'Mark selected products as active'

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} products marked as inactive.')
    mark_as_inactive.short_description = 'Mark selected products as inactive'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'order', 'image']
    list_filter = ['is_primary', 'product']
    search_fields = ['product__name', 'alt_text']
    list_editable = ['order']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant_name', 'order']
    list_filter = ['product']
    search_fields = ['product__name', 'variant_name', 'description']
    list_editable = ['order']


@admin.register(FragranceOption)
class FragranceOptionAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'category', 'order']
    list_filter = ['product', 'category']
    search_fields = ['product__name', 'name', 'description']
    list_editable = ['order']
