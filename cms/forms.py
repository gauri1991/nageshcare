from django import forms
from products.models import Product, Category
from .models import FeatureCard, CompanyStat
from inquiries.models import ContactMessage, QuoteRequest, InquiryReply


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


# ========================================
# Inquiry Management Forms
# ========================================

class ContactMessageReplyForm(forms.Form):
    """Form for replying to contact messages"""
    reply_subject = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re: Your inquiry about...'
        }),
        label='Subject'
    )
    reply_message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Type your reply message here...'
        }),
        label='Message'
    )

    def __init__(self, *args, **kwargs):
        contact_message = kwargs.pop('contact_message', None)
        super().__init__(*args, **kwargs)

        # Pre-populate subject if contact_message is provided
        if contact_message and not self.is_bound:
            self.fields['reply_subject'].initial = f"Re: {contact_message.get_subject_display()}"


class QuoteRequestReplyForm(forms.Form):
    """Form for replying to quote requests with optional attachment"""
    reply_subject = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quote for your inquiry - Reference: QR12345678'
        }),
        label='Subject'
    )
    reply_message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Type your quote details here...'
        }),
        label='Message'
    )
    attachment = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.xls,.xlsx'
        }),
        label='Attachment (Optional)',
        help_text='Attach quote PDF or document (max 10MB)'
    )

    def __init__(self, *args, **kwargs):
        quote_request = kwargs.pop('quote_request', None)
        super().__init__(*args, **kwargs)

        # Pre-populate subject if quote_request is provided
        if quote_request and not self.is_bound:
            self.fields['reply_subject'].initial = f"Quote for {quote_request.business_name} - Ref: {quote_request.reference_id}"


class ContactMessageStatusForm(forms.ModelForm):
    """Form for updating contact message status and admin notes"""

    class Meta:
        model = ContactMessage
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'admin_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Internal notes for team reference (not visible to customer)'
            }),
        }


class QuoteRequestStatusForm(forms.ModelForm):
    """Form for updating quote request status and admin notes"""

    class Meta:
        model = QuoteRequest
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'admin_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Internal notes for team reference (not visible to customer)'
            }),
        }
