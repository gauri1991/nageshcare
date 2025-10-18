from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Q

from .models import (
    SiteSettings, HeroSection, FeatureCard, TrustIndicator,
    Testimonial, ClientIndustry, CompanyStat, TextContent,
    CallToAction, MediaFile, ThemeSettings
)
from products.models import Product, Category, ProductImage
from inquiries.models import ContactMessage, QuoteRequest
from .forms import (
    ProductForm, CategoryForm, FeatureCardForm, CompanyStatForm,
    ContactMessageReplyForm, QuoteRequestReplyForm,
    ContactMessageStatusForm, QuoteRequestStatusForm
)


class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to require staff/superuser access"""

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_staff or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        return redirect('cms:login')


class CMSLoginView(LoginView):
    """Custom login view for CMS"""
    template_name = 'cms/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('cms:dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)


class DashboardView(StaffRequiredMixin, TemplateView):
    """Main CMS dashboard"""
    template_name = 'cms/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get quick stats
        context['stats'] = {
            'products': Product.objects.filter(is_active=True).count(),
            'testimonials': Testimonial.objects.filter(is_active=True).count(),
            'contact_messages': ContactMessage.objects.filter(status='new').count(),
            'quote_requests': QuoteRequest.objects.filter(status='new').count(),
        }

        # Recent activity
        context['recent_testimonials'] = Testimonial.objects.all()[:5]
        context['recent_messages'] = ContactMessage.objects.all()[:5]

        return context


class HomePageView(StaffRequiredMixin, TemplateView):
    """Edit home page content"""
    template_name = 'cms/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all home page sections
        context['hero'] = HeroSection.objects.filter(page_name='home').first()
        context['trust_indicators'] = TrustIndicator.objects.filter(position='hero', is_active=True)
        context['intro_text'] = TextContent.objects.filter(page_name='home', section_identifier='intro').first()
        context['product_range'] = TextContent.objects.filter(page_name='home', section_identifier='product-range').first()
        context['features'] = FeatureCard.objects.filter(section_identifier='why-choose-us', is_active=True)
        context['testimonials'] = Testimonial.objects.filter(is_active=True, is_featured=True)
        context['industries'] = ClientIndustry.objects.filter(is_active=True)
        context['stats'] = CompanyStat.objects.filter(section='home-testimonials', is_active=True)
        context['cta'] = CallToAction.objects.filter(page_name='home').first()

        return context

    def post(self, request, *args, **kwargs):
        section = request.POST.get('section')

        if section == 'hero':
            hero, created = HeroSection.objects.get_or_create(page_name='home')
            hero.title = request.POST.get('title', '')
            hero.subtitle = request.POST.get('subtitle', '')
            hero.description = request.POST.get('description', '')
            hero.content_alignment = request.POST.get('content_alignment', 'left')
            hero.button1_text = request.POST.get('button1_text', '')
            hero.button1_url = request.POST.get('button1_url', '')
            hero.button2_text = request.POST.get('button2_text', '')
            hero.button2_url = request.POST.get('button2_url', '')

            if request.FILES.get('background_image'):
                hero.background_image = request.FILES['background_image']

            hero.save()
            messages.success(request, 'Hero section updated successfully!')

        elif section == 'intro_text':
            intro, created = TextContent.objects.get_or_create(
                page_name='home',
                section_identifier='intro'
            )
            intro.title = request.POST.get('title', '')
            intro.content = request.POST.get('content', '')
            intro.save()
            messages.success(request, 'Introduction text updated successfully!')

        elif section == 'product_range':
            product_range, created = TextContent.objects.get_or_create(
                page_name='home',
                section_identifier='product-range'
            )
            product_range.title = request.POST.get('subtitle', '')
            product_range.content = request.POST.get('heading', '')
            product_range.save()
            messages.success(request, 'Product Range section updated successfully!')

        elif section == 'cta':
            cta, created = CallToAction.objects.get_or_create(page_name='home')
            cta.title = request.POST.get('title', '')
            cta.description = request.POST.get('description', '')
            cta.primary_button_text = request.POST.get('primary_button_text', '')
            cta.primary_button_url = request.POST.get('primary_button_url', '')
            cta.save()
            messages.success(request, 'Call to action updated successfully!')

        elif section == 'clear_hero_image':
            hero = HeroSection.objects.filter(page_name='home').first()
            if hero and hero.background_image:
                hero.background_image.delete()
                hero.background_image = None
                hero.save()
                messages.success(request, 'Background image removed. Now using theme gradient.')
            else:
                messages.info(request, 'No background image to remove.')

        return redirect('cms:page_home')


class AboutPageView(StaffRequiredMixin, TemplateView):
    """Edit about page content"""
    template_name = 'cms/pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['hero'] = HeroSection.objects.filter(page_name='about').first()
        context['company_story'] = TextContent.objects.filter(page_name='about', section_identifier='company-story').first()
        context['vision_mission'] = FeatureCard.objects.filter(section_identifier='about-vision-mission', is_active=True)
        context['how_we_work'] = FeatureCard.objects.filter(section_identifier='how-we-work', is_active=True)
        context['values'] = FeatureCard.objects.filter(section_identifier='values', is_active=True)
        context['cta'] = CallToAction.objects.filter(page_name='about').first()

        return context

    def post(self, request, *args, **kwargs):
        section = request.POST.get('section')

        if section == 'hero':
            hero, created = HeroSection.objects.get_or_create(page_name='about')
            hero.title = request.POST.get('title', '')
            hero.subtitle = request.POST.get('subtitle', '')
            hero.description = request.POST.get('description', '')
            hero.button1_text = request.POST.get('button1_text', '')
            hero.button1_url = request.POST.get('button1_url', '')

            if request.FILES.get('background_image'):
                hero.background_image = request.FILES['background_image']

            hero.save()
            messages.success(request, 'Hero section updated successfully!')

        elif section == 'company_story':
            story, created = TextContent.objects.get_or_create(
                page_name='about',
                section_identifier='company-story'
            )
            story.title = request.POST.get('title', '')
            story.content = request.POST.get('content', '')
            story.save()
            messages.success(request, 'Company story updated successfully!')

        elif section == 'cta':
            cta, created = CallToAction.objects.get_or_create(page_name='about')
            cta.title = request.POST.get('title', '')
            cta.description = request.POST.get('description', '')
            cta.primary_button_text = request.POST.get('primary_button_text', '')
            cta.primary_button_url = request.POST.get('primary_button_url', '')
            cta.save()
            messages.success(request, 'Call to action updated successfully!')

        elif section == 'clear_hero_image':
            hero = HeroSection.objects.filter(page_name='about').first()
            if hero and hero.background_image:
                hero.background_image.delete()
                hero.background_image = None
                hero.save()
                messages.success(request, 'Background image removed. Now using theme gradient.')
            else:
                messages.info(request, 'No background image to remove.')

        return redirect('cms:page_about')


class ContactPageView(StaffRequiredMixin, TemplateView):
    """Edit contact page content"""
    template_name = 'cms/pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['hero'] = HeroSection.objects.filter(page_name='contact').first()
        context['settings'] = SiteSettings.load()

        return context

    def post(self, request, *args, **kwargs):
        section = request.POST.get('section')

        if section == 'hero':
            hero, created = HeroSection.objects.get_or_create(page_name='contact')
            hero.title = request.POST.get('title', '')
            hero.subtitle = request.POST.get('subtitle', '')
            hero.description = request.POST.get('description', '')

            if request.FILES.get('background_image'):
                hero.background_image = request.FILES['background_image']

            hero.save()
            messages.success(request, 'Hero section updated successfully!')

        return redirect('cms:page_contact')


class ProductsPageView(StaffRequiredMixin, TemplateView):
    """Edit products page content"""
    template_name = 'cms/pages/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['hero'] = HeroSection.objects.filter(page_name='products').first()
        context['product_benefits'] = FeatureCard.objects.filter(section_identifier='product-benefits', is_active=True)
        context['cta'] = CallToAction.objects.filter(page_name='products').first()

        return context

    def post(self, request, *args, **kwargs):
        section = request.POST.get('section')

        if section == 'hero':
            hero, created = HeroSection.objects.get_or_create(page_name='products')
            hero.title = request.POST.get('title', '')
            hero.subtitle = request.POST.get('subtitle', '')
            hero.description = request.POST.get('description', '')
            hero.button1_text = request.POST.get('button1_text', '')
            hero.button1_url = request.POST.get('button1_url', '')
            hero.button2_text = request.POST.get('button2_text', '')
            hero.button2_url = request.POST.get('button2_url', '')

            if request.FILES.get('background_image'):
                hero.background_image = request.FILES['background_image']

            hero.save()
            messages.success(request, 'Hero section updated successfully!')

        elif section == 'cta':
            cta, created = CallToAction.objects.get_or_create(page_name='products')
            cta.title = request.POST.get('title', '')
            cta.description = request.POST.get('description', '')
            cta.primary_button_text = request.POST.get('primary_button_text', '')
            cta.primary_button_url = request.POST.get('primary_button_url', '')
            cta.save()
            messages.success(request, 'Call to action updated successfully!')

        return redirect('cms:page_products')


class RequestQuotePageView(StaffRequiredMixin, TemplateView):
    """Edit request quote page content"""
    template_name = 'cms/pages/request_quote.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['hero'] = HeroSection.objects.filter(page_name='request-quote').first()
        context['quote_inclusions'] = FeatureCard.objects.filter(section_identifier='quote-inclusions', is_active=True)
        context['contact_methods'] = TextContent.objects.filter(page_name='request-quote', section_identifier='contact-methods').first()
        context['cta'] = CallToAction.objects.filter(page_name='request-quote').first()

        return context

    def post(self, request, *args, **kwargs):
        section = request.POST.get('section')

        if section == 'hero':
            hero, created = HeroSection.objects.get_or_create(page_name='request-quote')
            hero.title = request.POST.get('title', '')
            hero.description = request.POST.get('description', '')

            # Metric 1: Using button1_text for value, button1_url for label, button2_text for icon
            hero.button1_text = request.POST.get('metric1_value', '')
            hero.button1_url = request.POST.get('metric1_label', '')
            hero.button2_text = request.POST.get('metric1_icon', '')

            # Metric 2: Using subtitle for value, button2_url for label, content_alignment for icon
            hero.subtitle = request.POST.get('metric2_value', '')
            hero.button2_url = request.POST.get('metric2_label', '')
            hero.content_alignment = request.POST.get('metric2_icon', '')

            # Metric 3: Using dedicated metric3 fields
            hero.metric3_value = request.POST.get('metric3_value', '')
            hero.metric3_label = request.POST.get('metric3_label', '')
            hero.metric3_icon = request.POST.get('metric3_icon', '')

            hero.save()
            messages.success(request, 'Hero section updated successfully!')

        elif section == 'contact_methods':
            contact_methods, created = TextContent.objects.get_or_create(
                page_name='request-quote',
                section_identifier='contact-methods'
            )
            contact_methods.title = request.POST.get('subtitle', '')
            contact_methods.content = request.POST.get('title', '')
            contact_methods.save()
            messages.success(request, 'Contact methods section updated successfully!')

        elif section == 'cta':
            cta, created = CallToAction.objects.get_or_create(page_name='request-quote')
            cta.title = request.POST.get('title', '')
            cta.description = request.POST.get('description', '')
            cta.save()
            messages.success(request, 'Call to action updated successfully!')

        return redirect('cms:page_request_quote')


class SiteSettingsView(StaffRequiredMixin, TemplateView):
    """Edit site-wide settings"""
    template_name = 'cms/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.load()
        context['theme'] = ThemeSettings.load()
        return context

    def post(self, request, *args, **kwargs):
        section = request.POST.get('section', '')

        # Handle theme settings
        if section == 'theme':
            theme = ThemeSettings.load()

            # Check if a palette was selected
            selected_palette = request.POST.get('active_palette', '')
            if selected_palette and selected_palette != 'custom':
                # Apply the selected palette
                theme.apply_palette(selected_palette)
                theme.active_palette = selected_palette
            else:
                # Custom palette - save individual fields
                theme.active_palette = 'custom'

                # Core Colors
                theme.primary_color = request.POST.get('primary_color', theme.primary_color)
                theme.primary_hover = request.POST.get('primary_hover', theme.primary_hover)
                theme.secondary_color = request.POST.get('secondary_color', theme.secondary_color)
                theme.secondary_hover = request.POST.get('secondary_hover', theme.secondary_hover)
                theme.accent_color = request.POST.get('accent_color', theme.accent_color)
                theme.background_light = request.POST.get('background_light', theme.background_light)
                theme.background_dark = request.POST.get('background_dark', theme.background_dark)
                theme.text_primary = request.POST.get('text_primary', theme.text_primary)
                theme.text_secondary = request.POST.get('text_secondary', theme.text_secondary)
                theme.border_light = request.POST.get('border_light', theme.border_light)
                theme.border_medium = request.POST.get('border_medium', theme.border_medium)

                # Header - Top Bar
                theme.topbar_bg = request.POST.get('topbar_bg', theme.topbar_bg)
                theme.topbar_text = request.POST.get('topbar_text', theme.topbar_text)
                theme.topbar_link = request.POST.get('topbar_link', theme.topbar_link)
                theme.topbar_link_hover = request.POST.get('topbar_link_hover', theme.topbar_link_hover)

                # Header - Navigation
                theme.navbar_bg = request.POST.get('navbar_bg', theme.navbar_bg)
                theme.navbar_link = request.POST.get('navbar_link', theme.navbar_link)
                theme.navbar_link_hover = request.POST.get('navbar_link_hover', theme.navbar_link_hover)
                theme.navbar_link_active = request.POST.get('navbar_link_active', theme.navbar_link_active)

                # Content
                theme.section_subtitle = request.POST.get('section_subtitle', theme.section_subtitle)
                theme.text_muted = request.POST.get('text_muted', theme.text_muted)

                # Icons
                theme.icon_default = request.POST.get('icon_default', theme.icon_default)
                theme.icon_hover = request.POST.get('icon_hover', theme.icon_hover)
                theme.icon_feature = request.POST.get('icon_feature', theme.icon_feature)
                theme.icon_trust = request.POST.get('icon_trust', theme.icon_trust)

                # Footer
                theme.footer_bg = request.POST.get('footer_bg', theme.footer_bg)
                theme.footer_heading = request.POST.get('footer_heading', theme.footer_heading)
                theme.footer_text = request.POST.get('footer_text', theme.footer_text)
                theme.footer_link = request.POST.get('footer_link', theme.footer_link)
                theme.footer_link_hover = request.POST.get('footer_link_hover', theme.footer_link_hover)
                theme.footer_icon = request.POST.get('footer_icon', theme.footer_icon)

                # Typography
                theme.font_heading = request.POST.get('font_heading', theme.font_heading)
                theme.font_heading_weight = int(request.POST.get('font_heading_weight', theme.font_heading_weight))
                theme.font_body = request.POST.get('font_body', theme.font_body)
                theme.font_body_weight = int(request.POST.get('font_body_weight', theme.font_body_weight))
                theme.font_size_base = request.POST.get('font_size_base', theme.font_size_base)
                theme.font_size_h1 = request.POST.get('font_size_h1', theme.font_size_h1)
                theme.font_size_h2 = request.POST.get('font_size_h2', theme.font_size_h2)
                theme.font_size_h3 = request.POST.get('font_size_h3', theme.font_size_h3)
                theme.font_size_h4 = request.POST.get('font_size_h4', theme.font_size_h4)
                theme.font_size_h5 = request.POST.get('font_size_h5', theme.font_size_h5)
                theme.font_size_h6 = request.POST.get('font_size_h6', theme.font_size_h6)

                # Spacing & Effects
                theme.border_radius = request.POST.get('border_radius', theme.border_radius)
                theme.box_shadow_default = request.POST.get('box_shadow_default', theme.box_shadow_default)
                theme.box_shadow_hover = request.POST.get('box_shadow_hover', theme.box_shadow_hover)

            theme.save()
            messages.success(request, 'Theme settings updated successfully!')
            return redirect('cms:settings')

        # Handle regular site settings
        settings = SiteSettings.load()

        # Business Information
        settings.business_name = request.POST.get('business_name', '')
        settings.tagline = request.POST.get('tagline', '')
        settings.business_description = request.POST.get('business_description', '')

        # Contact Information
        settings.phone_primary = request.POST.get('phone_primary', '')
        settings.phone_whatsapp = request.POST.get('phone_whatsapp', '')
        settings.email_primary = request.POST.get('email_primary', '')
        settings.email_support = request.POST.get('email_support', '')
        settings.email_sales = request.POST.get('email_sales', '')

        # Business Hours
        settings.business_hours = request.POST.get('business_hours', '')

        # Address
        settings.address_line1 = request.POST.get('address_line1', '')
        settings.address_line2 = request.POST.get('address_line2', '')
        settings.city = request.POST.get('city', '')
        settings.state = request.POST.get('state', '')
        settings.pincode = request.POST.get('pincode', '')
        settings.map_embed_url = request.POST.get('map_embed_url', '')

        # Social Media
        settings.facebook_url = request.POST.get('facebook_url', '')
        settings.instagram_url = request.POST.get('instagram_url', '')
        settings.linkedin_url = request.POST.get('linkedin_url', '')
        settings.whatsapp_url = request.POST.get('whatsapp_url', '')

        # Business Details
        settings.gst_number = request.POST.get('gst_number', '')
        settings.cin_number = request.POST.get('cin_number', '')
        settings.msme_number = request.POST.get('msme_number', '')
        settings.established_year = request.POST.get('established_year', '')

        # SEO
        settings.default_meta_description = request.POST.get('default_meta_description', '')
        settings.default_meta_keywords = request.POST.get('default_meta_keywords', '')

        # Email Configuration
        settings.email_host = request.POST.get('email_host', '')
        settings.email_port = int(request.POST.get('email_port', 587))
        settings.email_use_tls = request.POST.get('email_use_tls') == '1'
        settings.email_host_user = request.POST.get('email_host_user', '')
        settings.email_host_password = request.POST.get('email_host_password', '')
        settings.email_reply_signature = request.POST.get('email_reply_signature', '')

        # WhatsApp Float Settings
        settings.whatsapp_float_enabled = request.POST.get('whatsapp_float_enabled') == '1'
        settings.whatsapp_float_message = request.POST.get('whatsapp_float_message', "Hi, I'm interested in your wholesale products. Please share more details.")
        settings.whatsapp_float_position_bottom = int(request.POST.get('whatsapp_float_position_bottom', 100))
        settings.whatsapp_float_position_right = int(request.POST.get('whatsapp_float_position_right', 20))
        settings.whatsapp_float_show_on_mobile = request.POST.get('whatsapp_float_show_on_mobile') == '1'
        settings.whatsapp_float_show_on_desktop = request.POST.get('whatsapp_float_show_on_desktop') == '1'

        settings.save()
        messages.success(request, 'Site settings updated successfully!')
        return redirect('cms:settings')


# Testimonials CRUD
class TestimonialListView(StaffRequiredMixin, ListView):
    """List all testimonials"""
    model = Testimonial
    template_name = 'cms/testimonials.html'
    context_object_name = 'testimonials'
    paginate_by = 20
    ordering = ['-is_featured', 'order', '-created_at']


class TestimonialCreateView(StaffRequiredMixin, CreateView):
    """Add new testimonial"""
    model = Testimonial
    template_name = 'cms/testimonial_form.html'
    fields = [
        'customer_name', 'customer_role', 'customer_location',
        'rating', 'testimonial_text', 'avatar_initials',
        'is_featured', 'is_active', 'order'
    ]
    success_url = reverse_lazy('cms:testimonials')

    def form_valid(self, form):
        messages.success(self.request, 'Testimonial added successfully!')
        return super().form_valid(form)


class TestimonialUpdateView(StaffRequiredMixin, UpdateView):
    """Edit testimonial"""
    model = Testimonial
    template_name = 'cms/testimonial_form.html'
    fields = [
        'customer_name', 'customer_role', 'customer_location',
        'rating', 'testimonial_text', 'avatar_initials',
        'is_featured', 'is_active', 'order'
    ]
    success_url = reverse_lazy('cms:testimonials')

    def form_valid(self, form):
        messages.success(self.request, 'Testimonial updated successfully!')
        return super().form_valid(form)


class TestimonialDeleteView(StaffRequiredMixin, DeleteView):
    """Delete testimonial"""
    model = Testimonial
    success_url = reverse_lazy('cms:testimonials')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Testimonial deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Client Industries CRUD
class ClientIndustryListView(StaffRequiredMixin, ListView):
    """List all client industries"""
    model = ClientIndustry
    template_name = 'cms/industries.html'
    context_object_name = 'industries'
    ordering = ['order', 'industry_name']


class ClientIndustryCreateView(StaffRequiredMixin, CreateView):
    """Add new industry"""
    model = ClientIndustry
    template_name = 'cms/industry_form.html'
    fields = ['industry_name', 'icon_class', 'description', 'order', 'is_active']
    success_url = reverse_lazy('cms:industries')

    def form_valid(self, form):
        messages.success(self.request, 'Industry added successfully!')
        return super().form_valid(form)


class ClientIndustryUpdateView(StaffRequiredMixin, UpdateView):
    """Edit industry"""
    model = ClientIndustry
    template_name = 'cms/industry_form.html'
    fields = ['industry_name', 'icon_class', 'description', 'order', 'is_active']
    success_url = reverse_lazy('cms:industries')

    def form_valid(self, form):
        messages.success(self.request, 'Industry updated successfully!')
        return super().form_valid(form)


class ClientIndustryDeleteView(StaffRequiredMixin, DeleteView):
    """Delete industry"""
    model = ClientIndustry
    success_url = reverse_lazy('cms:industries')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Industry deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Trust Indicators CRUD
class TrustIndicatorListView(StaffRequiredMixin, ListView):
    """List all trust indicators"""
    model = TrustIndicator
    template_name = 'cms/trust_badges.html'
    context_object_name = 'trust_badges'
    ordering = ['position', 'order']


class TrustIndicatorCreateView(StaffRequiredMixin, CreateView):
    """Add new trust indicator"""
    model = TrustIndicator
    template_name = 'cms/trust_badge_form.html'
    fields = ['title', 'subtitle', 'icon_class', 'position', 'order', 'is_active']
    success_url = reverse_lazy('cms:trust_badges')

    def form_valid(self, form):
        messages.success(self.request, 'Trust badge added successfully!')
        return super().form_valid(form)


class TrustIndicatorUpdateView(StaffRequiredMixin, UpdateView):
    """Edit trust indicator"""
    model = TrustIndicator
    template_name = 'cms/trust_badge_form.html'
    fields = ['title', 'subtitle', 'icon_class', 'position', 'order', 'is_active']
    success_url = reverse_lazy('cms:trust_badges')

    def form_valid(self, form):
        messages.success(self.request, 'Trust badge updated successfully!')
        return super().form_valid(form)


class TrustIndicatorDeleteView(StaffRequiredMixin, DeleteView):
    """Delete trust indicator"""
    model = TrustIndicator
    success_url = reverse_lazy('cms:trust_badges')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Trust badge deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Feature Cards CRUD
class FeatureCardListView(StaffRequiredMixin, ListView):
    """List all feature cards"""
    model = FeatureCard
    template_name = 'cms/feature_cards.html'
    context_object_name = 'feature_cards'
    ordering = ['section_identifier', 'order']

    def get_queryset(self):
        queryset = FeatureCard.objects.all()

        # Filter by section
        section = self.request.GET.get('section', '')
        if section:
            queryset = queryset.filter(section_identifier=section)

        # Filter by status
        status = self.request.GET.get('status', '')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset.order_by('section_identifier', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_section'] = self.request.GET.get('section', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['section_choices'] = FeatureCard.SECTION_CHOICES
        return context


class FeatureCardCreateView(StaffRequiredMixin, CreateView):
    """Add new feature card"""
    model = FeatureCard
    form_class = FeatureCardForm
    template_name = 'cms/feature_card_form.html'
    success_url = reverse_lazy('cms:feature_cards')

    def form_valid(self, form):
        messages.success(self.request, 'Feature card added successfully!')
        return super().form_valid(form)


class FeatureCardUpdateView(StaffRequiredMixin, UpdateView):
    """Edit feature card"""
    model = FeatureCard
    form_class = FeatureCardForm
    template_name = 'cms/feature_card_form.html'
    success_url = reverse_lazy('cms:feature_cards')

    def form_valid(self, form):
        messages.success(self.request, 'Feature card updated successfully!')
        return super().form_valid(form)


class FeatureCardDeleteView(StaffRequiredMixin, DeleteView):
    """Delete feature card"""
    model = FeatureCard
    success_url = reverse_lazy('cms:feature_cards')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Feature card deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Company Stats CRUD
class CompanyStatListView(StaffRequiredMixin, ListView):
    """List all company statistics"""
    model = CompanyStat
    template_name = 'cms/company_stats.html'
    context_object_name = 'stats'
    ordering = ['section', 'order']

    def get_queryset(self):
        queryset = CompanyStat.objects.all()

        # Filter by section
        section = self.request.GET.get('section', '')
        if section:
            queryset = queryset.filter(section=section)

        # Filter by status
        status = self.request.GET.get('status', '')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset.order_by('section', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_section'] = self.request.GET.get('section', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['section_choices'] = CompanyStat.SECTION_CHOICES
        return context


class CompanyStatCreateView(StaffRequiredMixin, CreateView):
    """Add new company statistic"""
    model = CompanyStat
    form_class = CompanyStatForm
    template_name = 'cms/company_stat_form.html'
    success_url = reverse_lazy('cms:company_stats')

    def form_valid(self, form):
        messages.success(self.request, 'Company statistic added successfully!')
        return super().form_valid(form)


class CompanyStatUpdateView(StaffRequiredMixin, UpdateView):
    """Edit company statistic"""
    model = CompanyStat
    form_class = CompanyStatForm
    template_name = 'cms/company_stat_form.html'
    success_url = reverse_lazy('cms:company_stats')

    def form_valid(self, form):
        messages.success(self.request, 'Company statistic updated successfully!')
        return super().form_valid(form)


class CompanyStatDeleteView(StaffRequiredMixin, DeleteView):
    """Delete company statistic"""
    model = CompanyStat
    success_url = reverse_lazy('cms:company_stats')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Company statistic deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Product Management
class ProductListView(StaffRequiredMixin, ListView):
    """List all products with search and filtering"""
    model = Product
    template_name = 'cms/products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.select_related('category').prefetch_related('images')
        
        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        # Filter by category
        category_id = self.request.GET.get('category', '')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by status
        status = self.request.GET.get('status', '')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        elif status == 'featured':
            queryset = queryset.filter(is_featured=True)
        elif status == 'coming_soon':
            queryset = queryset.filter(is_coming_soon=True)
        
        return queryset.order_by('-is_featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class ProductCreateView(StaffRequiredMixin, CreateView):
    """Create a new product"""
    model = Product
    form_class = ProductForm
    template_name = 'cms/products/product_form.html'
    success_url = reverse_lazy('cms:products')

    def form_valid(self, form):
        messages.success(self.request, f'Product "{form.instance.name}" created successfully!')
        return super().form_valid(form)


class ProductUpdateView(StaffRequiredMixin, UpdateView):
    """Edit an existing product"""
    model = Product
    form_class = ProductForm
    template_name = 'cms/products/product_form.html'
    success_url = reverse_lazy('cms:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Product "{form.instance.name}" updated successfully!')
        return super().form_valid(form)


class ProductDeleteView(StaffRequiredMixin, DeleteView):
    """Delete a product"""
    model = Product
    success_url = reverse_lazy('cms:products')
    
    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product_name = product.name
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Category Management
class CategoryListView(StaffRequiredMixin, ListView):
    """List all product categories"""
    model = Category
    template_name = 'cms/products/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Category.objects.annotate(product_count=Count('products'))
        
        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        # Filter by status
        status = self.request.GET.get('status', '')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class CategoryCreateView(StaffRequiredMixin, CreateView):
    """Create a new category"""
    model = Category
    form_class = CategoryForm
    template_name = 'cms/products/category_form.html'
    success_url = reverse_lazy('cms:categories')

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" created successfully!')
        return super().form_valid(form)


class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    """Edit an existing category"""
    model = Category
    form_class = CategoryForm
    template_name = 'cms/products/category_form.html'
    success_url = reverse_lazy('cms:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        context['product_count'] = self.object.products.count()
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" updated successfully!')
        return super().form_valid(form)


class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    """Delete a category"""
    model = Category
    success_url = reverse_lazy('cms:categories')
    
    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        product_count = category.products.count()
        
        if product_count > 0:
            messages.error(request, f'Cannot delete category "{category.name}" because it has {product_count} products. Please reassign or delete the products first.')
            return redirect('cms:categories')
        
        category_name = category.name
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Product Image Management
class ProductImageDeleteView(StaffRequiredMixin, DeleteView):
    """Delete a product image"""
    model = ProductImage

    def get_success_url(self):
        return reverse_lazy('cms:product_edit', kwargs={'pk': self.object.product.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Image deleted successfully!')
        return super().delete(request, *args, **kwargs)


def product_image_add(request, pk):
    """Upload new product images"""
    if not request.user.is_staff:
        return redirect('cms:login')

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        images = request.FILES.getlist('images')
        alt_text = request.POST.get('alt_text', '')
        set_as_primary = request.POST.get('set_as_primary') == 'on'

        if not images:
            messages.error(request, 'Please select at least one image to upload.')
            return redirect('cms:product_edit', pk=pk)

        # Check if product has a primary image
        has_primary = product.images.filter(is_primary=True).exists()

        # Get current image count for order calculation
        current_count = product.images.count()

        uploaded_count = 0
        try:
            for i, image in enumerate(images):
                # Create product image
                product_image = ProductImage(
                    product=product,
                    image=image,
                    alt_text=alt_text if alt_text else product.name,
                    order=current_count + i
                )

                # Set first image as primary if requested and no primary exists
                if i == 0 and set_as_primary and not has_primary:
                    product_image.is_primary = True
                    has_primary = True

                product_image.save()
                uploaded_count += 1

            if uploaded_count == 1:
                messages.success(request, 'Image uploaded successfully!')
            else:
                messages.success(request, f'{uploaded_count} images uploaded successfully!')
        except Exception as e:
            messages.error(request, f'Error uploading images: {str(e)}')

    return redirect('cms:product_edit', pk=pk)


def product_image_set_primary(request, pk):
    """Set a product image as primary"""
    if not request.user.is_staff:
        return redirect('cms:login')

    image = get_object_or_404(ProductImage, pk=pk)
    product = image.product

    if request.method == 'POST':
        # Remove primary status from all images of this product
        product.images.update(is_primary=False)

        # Set this image as primary
        image.is_primary = True
        image.save()

        messages.success(request, 'Primary image updated successfully!')

    return redirect('cms:product_edit', pk=product.pk)


# ========================================
# Inquiry Management - Contact Messages
# ========================================

class ContactMessageListView(StaffRequiredMixin, ListView):
    """List all contact messages with filtering"""
    model = ContactMessage
    template_name = 'cms/inquiries/contact_message_list.html'
    context_object_name = 'messages'
    paginate_by = 20

    def get_queryset(self):
        queryset = ContactMessage.objects.all()

        # Search by name or email
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(business_name__icontains=search_query)
            )

        # Filter by status
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by subject
        subject = self.request.GET.get('subject', '')
        if subject:
            queryset = queryset.filter(subject=subject)

        # Filter by read status
        is_read = self.request.GET.get('is_read', '')
        if is_read == 'yes':
            queryset = queryset.filter(is_read=True)
        elif is_read == 'no':
            queryset = queryset.filter(is_read=False)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_subject'] = self.request.GET.get('subject', '')
        context['selected_is_read'] = self.request.GET.get('is_read', '')
        context['status_choices'] = ContactMessage.STATUS_CHOICES
        context['subject_choices'] = ContactMessage.SUBJECT_CHOICES

        # Statistics
        context['stats'] = {
            'total': ContactMessage.objects.count(),
            'new': ContactMessage.objects.filter(status='new').count(),
            'unread': ContactMessage.objects.filter(is_read=False).count(),
            'contacted': ContactMessage.objects.filter(status='contacted').count(),
        }

        return context


class ContactMessageDetailView(StaffRequiredMixin, TemplateView):
    """View contact message details and send reply"""
    template_name = 'cms/inquiries/contact_message_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = get_object_or_404(ContactMessage, pk=kwargs['pk'])

        # Mark as read when viewed
        if not message.is_read:
            message.is_read = True
            message.save()

        context['message'] = message
        context['reply_form'] = ContactMessageReplyForm(contact_message=message)
        context['status_form'] = ContactMessageStatusForm(instance=message)
        context['replies'] = message.replies.all().order_by('-replied_at')

        return context

    def post(self, request, *args, **kwargs):
        from inquiries.email_utils import send_inquiry_reply
        from django.http import JsonResponse

        message = get_object_or_404(ContactMessage, pk=kwargs['pk'])
        action = request.POST.get('action', '')

        # Handle status update
        if action == 'update_status':
            status_form = ContactMessageStatusForm(request.POST, instance=message)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Status updated successfully!')
            else:
                messages.error(request, 'Failed to update status.')
            return redirect('cms:contact_message_detail', pk=message.pk)

        # Handle reply
        elif action == 'send_reply':
            reply_form = ContactMessageReplyForm(request.POST, contact_message=message)
            if reply_form.is_valid():
                result = send_inquiry_reply(
                    inquiry_type='contact',
                    inquiry_id=message.pk,
                    subject=reply_form.cleaned_data['reply_subject'],
                    message=reply_form.cleaned_data['reply_message'],
                    replied_by_user=request.user
                )

                if result['success']:
                    # Update message status
                    if message.status == 'new':
                        message.status = 'contacted'
                        message.save()

                    messages.success(
                        request,
                        f'Reply sent successfully to {result["recipient"]} ({result["recipient_email"]})'
                    )
                else:
                    messages.error(request, f'Failed to send reply: {result["error"]}')
            else:
                messages.error(request, 'Please correct the form errors.')

            return redirect('cms:contact_message_detail', pk=message.pk)

        return redirect('cms:contact_message_detail', pk=message.pk)


class ContactMessageDeleteView(StaffRequiredMixin, DeleteView):
    """Delete a contact message"""
    model = ContactMessage
    success_url = reverse_lazy('cms:contact_messages')

    def delete(self, request, *args, **kwargs):
        message = self.get_object()
        name = message.name
        messages.success(request, f'Contact message from {name} deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ========================================
# Inquiry Management - Quote Requests
# ========================================

class QuoteRequestListView(StaffRequiredMixin, ListView):
    """List all quote requests with filtering"""
    model = QuoteRequest
    template_name = 'cms/inquiries/quote_request_list.html'
    context_object_name = 'quotes'
    paginate_by = 20

    def get_queryset(self):
        queryset = QuoteRequest.objects.all()

        # Search by name, email, or business name
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(business_name__icontains=search_query) |
                Q(reference_id__icontains=search_query)
            )

        # Filter by status
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by business type
        business_type = self.request.GET.get('business_type', '')
        if business_type:
            queryset = queryset.filter(business_type=business_type)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_business_type'] = self.request.GET.get('business_type', '')
        context['status_choices'] = QuoteRequest.STATUS_CHOICES
        context['business_type_choices'] = QuoteRequest.BUSINESS_TYPE_CHOICES

        # Statistics
        context['stats'] = {
            'total': QuoteRequest.objects.count(),
            'new': QuoteRequest.objects.filter(status='new').count(),
            'reviewing': QuoteRequest.objects.filter(status='reviewing').count(),
            'quoted': QuoteRequest.objects.filter(status='quoted').count(),
        }

        return context


class QuoteRequestDetailView(StaffRequiredMixin, TemplateView):
    """View quote request details and send reply"""
    template_name = 'cms/inquiries/quote_request_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quote = get_object_or_404(QuoteRequest, pk=kwargs['pk'])

        context['quote'] = quote
        context['reply_form'] = QuoteRequestReplyForm(quote_request=quote)
        context['status_form'] = QuoteRequestStatusForm(instance=quote)
        context['replies'] = quote.replies.all().order_by('-replied_at')

        return context

    def post(self, request, *args, **kwargs):
        from inquiries.email_utils import send_inquiry_reply
        from django.http import JsonResponse

        quote = get_object_or_404(QuoteRequest, pk=kwargs['pk'])
        action = request.POST.get('action', '')

        # Handle status update
        if action == 'update_status':
            status_form = QuoteRequestStatusForm(request.POST, instance=quote)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Status updated successfully!')
            else:
                messages.error(request, 'Failed to update status.')
            return redirect('cms:quote_request_detail', pk=quote.pk)

        # Handle reply with attachment
        elif action == 'send_reply':
            reply_form = QuoteRequestReplyForm(request.POST, request.FILES, quote_request=quote)
            if reply_form.is_valid():
                attachment = request.FILES.get('attachment', None)

                result = send_inquiry_reply(
                    inquiry_type='quote',
                    inquiry_id=quote.pk,
                    subject=reply_form.cleaned_data['reply_subject'],
                    message=reply_form.cleaned_data['reply_message'],
                    replied_by_user=request.user,
                    attachment_file=attachment
                )

                if result['success']:
                    # Update quote status
                    if quote.status == 'new':
                        quote.status = 'quoted'
                        quote.save()
                    elif quote.status == 'reviewing':
                        quote.status = 'quoted'
                        quote.save()

                    messages.success(
                        request,
                        f'Quote sent successfully to {result["recipient"]} ({result["recipient_email"]})'
                    )
                else:
                    messages.error(request, f'Failed to send reply: {result["error"]}')
            else:
                messages.error(request, 'Please correct the form errors.')

            return redirect('cms:quote_request_detail', pk=quote.pk)

        return redirect('cms:quote_request_detail', pk=quote.pk)


class QuoteRequestDeleteView(StaffRequiredMixin, DeleteView):
    """Delete a quote request"""
    model = QuoteRequest
    success_url = reverse_lazy('cms:quote_requests')

    def delete(self, request, *args, **kwargs):
        quote = self.get_object()
        business_name = quote.business_name
        messages.success(request, f'Quote request from {business_name} deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ========================================
# CSV Export Functions
# ========================================

def export_contact_messages_csv(request):
    """Export contact messages to CSV"""
    import csv
    from django.http import HttpResponse
    from datetime import datetime

    if not request.user.is_staff:
        return redirect('cms:login')

    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="contact_messages_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'

    writer = csv.writer(response)

    # Write header
    writer.writerow([
        'ID', 'Date', 'Name', 'Email', 'Phone', 'Business Name',
        'Subject', 'Message', 'Status', 'Is Read', 'Reply Count'
    ])

    # Get filtered queryset (respect filters from request)
    queryset = ContactMessage.objects.all()

    # Apply same filters as list view
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(business_name__icontains=search_query)
        )

    status = request.GET.get('status', '')
    if status:
        queryset = queryset.filter(status=status)

    subject = request.GET.get('subject', '')
    if subject:
        queryset = queryset.filter(subject=subject)

    is_read = request.GET.get('is_read', '')
    if is_read == 'yes':
        queryset = queryset.filter(is_read=True)
    elif is_read == 'no':
        queryset = queryset.filter(is_read=False)

    queryset = queryset.order_by('-created_at')

    # Write data rows
    for msg in queryset:
        writer.writerow([
            msg.id,
            msg.created_at.strftime('%Y-%m-%d %H:%M'),
            msg.name,
            msg.email,
            msg.phone or '',
            msg.business_name or '',
            msg.get_subject_display(),
            msg.message,
            msg.get_status_display(),
            'Yes' if msg.is_read else 'No',
            msg.replies.count()
        ])

    return response


def export_quote_requests_csv(request):
    """Export quote requests to CSV"""
    import csv
    from django.http import HttpResponse
    from datetime import datetime

    if not request.user.is_staff:
        return redirect('cms:login')

    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="quote_requests_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'

    writer = csv.writer(response)

    # Write header
    writer.writerow([
        'Reference ID', 'Date', 'Name', 'Email', 'Phone', 'Business Name', 'Business Type',
        'Product Type', 'Quantity', 'Budget Range', 'Custom Branding', 'Sample Order',
        'Delivery State', 'Delivery City', 'Order Frequency', 'Status', 'Reply Count'
    ])

    # Get filtered queryset (respect filters from request)
    queryset = QuoteRequest.objects.all()

    # Apply same filters as list view
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(business_name__icontains=search_query) |
            Q(reference_id__icontains=search_query)
        )

    status = request.GET.get('status', '')
    if status:
        queryset = queryset.filter(status=status)

    business_type = request.GET.get('business_type', '')
    if business_type:
        queryset = queryset.filter(business_type=business_type)

    queryset = queryset.order_by('-created_at')

    # Write data rows
    for quote in queryset:
        writer.writerow([
            quote.reference_id,
            quote.created_at.strftime('%Y-%m-%d %H:%M'),
            quote.name,
            quote.email,
            quote.phone or '',
            quote.business_name,
            quote.get_business_type_display(),
            quote.product_type or '',
            quote.quantity or '',
            quote.budget_range or '',
            'Yes' if quote.need_custom_branding else 'No',
            'Yes' if quote.sample_order_interest else 'No',
            quote.delivery_state or '',
            quote.delivery_city or '',
            quote.order_frequency or '',
            quote.get_status_display(),
            quote.replies.count()
        ])

    return response


# ========================================
# Policy Document Management
# ========================================

class PrivacyPolicyView(StaffRequiredMixin, TemplateView):
    """Edit Privacy Policy"""
    template_name = 'cms/policies/privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['policy'] = TextContent.objects.filter(
            page_name='policies',
            section_identifier='privacy-policy'
        ).first()
        return context

    def post(self, request, *args, **kwargs):
        policy, created = TextContent.objects.get_or_create(
            page_name='policies',
            section_identifier='privacy-policy'
        )
        policy.title = request.POST.get('title', 'Privacy Policy')
        policy.content = request.POST.get('content', '')
        policy.save()
        messages.success(request, 'Privacy Policy updated successfully!')
        return redirect('cms:privacy_policy')


class TermsConditionsView(StaffRequiredMixin, TemplateView):
    """Edit Terms & Conditions"""
    template_name = 'cms/policies/terms_conditions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['policy'] = TextContent.objects.filter(
            page_name='policies',
            section_identifier='terms-conditions'
        ).first()
        return context

    def post(self, request, *args, **kwargs):
        policy, created = TextContent.objects.get_or_create(
            page_name='policies',
            section_identifier='terms-conditions'
        )
        policy.title = request.POST.get('title', 'Terms & Conditions')
        policy.content = request.POST.get('content', '')
        policy.save()
        messages.success(request, 'Terms & Conditions updated successfully!')
        return redirect('cms:terms_conditions')


class RefundPolicyView(StaffRequiredMixin, TemplateView):
    """Edit Refund Policy"""
    template_name = 'cms/policies/refund_policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['policy'] = TextContent.objects.filter(
            page_name='policies',
            section_identifier='refund-policy'
        ).first()
        return context

    def post(self, request, *args, **kwargs):
        policy, created = TextContent.objects.get_or_create(
            page_name='policies',
            section_identifier='refund-policy'
        )
        policy.title = request.POST.get('title', 'Refund Policy')
        policy.content = request.POST.get('content', '')
        policy.save()
        messages.success(request, 'Refund Policy updated successfully!')
        return redirect('cms:refund_policy')


def theme_css(request):
    """Serve dynamic theme CSS"""
    from django.http import HttpResponse
    from django.template.loader import render_to_string

    theme = ThemeSettings.load()

    css_content = render_to_string('cms/theme.css', {'theme': theme})

    return HttpResponse(css_content, content_type='text/css')
