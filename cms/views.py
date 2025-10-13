from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count

from .models import (
    SiteSettings, HeroSection, FeatureCard, TrustIndicator,
    Testimonial, ClientIndustry, CompanyStat, TextContent,
    CallToAction, MediaFile
)
from products.models import Product, Category, ProductImage
from inquiries.models import ContactMessage, QuoteRequest
from .forms import ProductForm, CategoryForm, FeatureCardForm, CompanyStatForm


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

        elif section == 'cta':
            cta, created = CallToAction.objects.get_or_create(page_name='home')
            cta.title = request.POST.get('title', '')
            cta.description = request.POST.get('description', '')
            cta.primary_button_text = request.POST.get('primary_button_text', '')
            cta.primary_button_url = request.POST.get('primary_button_url', '')
            cta.save()
            messages.success(request, 'Call to action updated successfully!')

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


class SiteSettingsView(StaffRequiredMixin, TemplateView):
    """Edit site-wide settings"""
    template_name = 'cms/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.load()
        return context

    def post(self, request, *args, **kwargs):
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
