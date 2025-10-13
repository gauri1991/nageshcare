from django import forms
from products.models import Product, Category
from .models import FeatureCard, CompanyStat


class ProductForm(forms.ModelForm):
    """Form for creating and editing products with proper Bootstrap styling"""

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'tagline', 'short_description', 'full_description',
            'features', 'brand_name', 'minimum_order_quantity',
            'is_featured', 'is_coming_soon', 'is_active',
            'meta_title', 'meta_description', 'meta_keywords'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Short catchy tagline'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description for catalog/listing page'
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Detailed description for product detail page'
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List product features, one per line'
            }),
            'brand_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brand name (optional)'
            }),
            'minimum_order_quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 500 packs or 1,000 sticks'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_coming_soon': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Leave blank to use product name'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'SEO description (max 160 characters)'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Comma-separated keywords'
            }),
        }


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories with proper Bootstrap styling"""

    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Personal Care Products'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Brief description of what products belong in this category'
            }),
            'icon': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class FeatureCardForm(forms.ModelForm):
    """Form for creating and editing feature cards with proper Bootstrap styling"""

    class Meta:
        model = FeatureCard
        fields = ['section_identifier', 'title', 'description', 'icon_class', 'order', 'is_active']
        widgets = {
            'section_identifier': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Quality Assured Products'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed description of this feature or value'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., bi bi-award-fill'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class CompanyStatForm(forms.ModelForm):
    """Form for creating and editing company statistics with proper Bootstrap styling"""

    class Meta:
        model = CompanyStat
        fields = ['label', 'value', 'icon_class', 'section', 'order', 'is_active']
        widgets = {
            'label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Happy Clients'
            }),
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 500+'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., bi bi-people-fill (optional)'
            }),
            'section': forms.Select(attrs={
                'class': 'form-select'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
