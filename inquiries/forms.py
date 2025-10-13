from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from crispy_forms.bootstrap import FormActions
from .models import ContactMessage, Inquiry, QuoteRequest


class ContactForm(forms.ModelForm):
    """Contact form with crispy forms styling"""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-3'),
                Column('subject', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'message',
            FormActions(
                Submit('submit', 'Send Message', css_class='btn btn-secondary-custom btn-lg px-5')
            )
        )


class InquiryForm(forms.ModelForm):
    """Product inquiry form"""

    class Meta:
        model = Inquiry
        fields = ['product', 'name', 'business_name', 'email', 'phone', 'quantity_needed', 'delivery_location', 'additional_requirements']
        widgets = {
            'product': forms.HiddenInput(),
            'additional_requirements': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'product',
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('business_name', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-3'),
                Column('phone', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('quantity_needed', css_class='form-group col-md-6 mb-3'),
                Column('delivery_location', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'additional_requirements',
            FormActions(
                Submit('submit', 'Submit Inquiry', css_class='btn btn-primary-custom btn-lg')
            )
        )


class QuoteRequestForm(forms.ModelForm):
    """Detailed quote request form"""

    class Meta:
        model = QuoteRequest
        exclude = ['reference_id', 'created_at', 'updated_at', 'status', 'admin_notes', 'logo_file']
        widgets = {
            'product_interests': forms.Textarea(attrs={'rows': 3}),
            'branding_requirements': forms.Textarea(attrs={'rows': 3}),
            'specific_requirements': forms.Textarea(attrs={'rows': 3}),
            'special_delivery_requirements': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h4 class="text-primary-custom mb-3">Business Information</h4>'),
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('business_name', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('business_type', css_class='form-group col-md-6 mb-3'),
                Column('years_in_business', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),

            HTML('<h4 class="text-primary-custom mt-4 mb-3">Contact Information</h4>'),
            Row(
                Column('email', css_class='form-group col-md-6 mb-3'),
                Column('phone', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('whatsapp_number', css_class='form-group col-md-6 mb-3'),
                Column('preferred_contact_method', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),

            HTML('<h4 class="text-primary-custom mt-4 mb-3">Product Requirements</h4>'),
            'product_interests',
            Row(
                Column('order_frequency', css_class='form-group col-md-6 mb-3'),
                Column('sample_order_first', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),

            HTML('<h4 class="text-primary-custom mt-4 mb-3">White-Label Branding (Optional)</h4>'),
            Row(
                Column('custom_branding_required', css_class='form-group col-md-6 mb-3'),
                Column('brand_name', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'branding_requirements',

            HTML('<h4 class="text-primary-custom mt-4 mb-3">Delivery & Additional Details</h4>'),
            Row(
                Column('delivery_city', css_class='form-group col-md-4 mb-3'),
                Column('delivery_state', css_class='form-group col-md-4 mb-3'),
                Column('delivery_pin', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            'payment_terms_preference',
            'specific_requirements',

            FormActions(
                Submit('submit', 'Submit Quote Request', css_class='btn btn-secondary-custom btn-lg px-5 mt-4')
            )
        )
