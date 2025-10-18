from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'cms'

urlpatterns = [
    # Authentication
    path('login/', views.CMSLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/cms/login/'), name='logout'),

    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard_alt'),

    # Page Editing
    path('pages/home/', views.HomePageView.as_view(), name='page_home'),
    path('pages/about/', views.AboutPageView.as_view(), name='page_about'),
    path('pages/contact/', views.ContactPageView.as_view(), name='page_contact'),
    path('pages/products/', views.ProductsPageView.as_view(), name='page_products'),
    path('pages/request-quote/', views.RequestQuotePageView.as_view(), name='page_request_quote'),

    # Policy Documents
    path('policies/privacy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('policies/terms/', views.TermsConditionsView.as_view(), name='terms_conditions'),
    path('policies/refund/', views.RefundPolicyView.as_view(), name='refund_policy'),

    # Settings
    path('settings/', views.SiteSettingsView.as_view(), name='settings'),
    path('theme.css', views.theme_css, name='theme_css'),

    # Testimonials Management
    path('testimonials/', views.TestimonialListView.as_view(), name='testimonials'),
    path('testimonials/add/', views.TestimonialCreateView.as_view(), name='testimonial_add'),
    path('testimonials/<int:pk>/edit/', views.TestimonialUpdateView.as_view(), name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', views.TestimonialDeleteView.as_view(), name='testimonial_delete'),

    # Industries Management
    path('industries/', views.ClientIndustryListView.as_view(), name='industries'),
    path('industries/add/', views.ClientIndustryCreateView.as_view(), name='industry_add'),
    path('industries/<int:pk>/edit/', views.ClientIndustryUpdateView.as_view(), name='industry_edit'),
    path('industries/<int:pk>/delete/', views.ClientIndustryDeleteView.as_view(), name='industry_delete'),

    # Trust Badges Management
    path('trust-badges/', views.TrustIndicatorListView.as_view(), name='trust_badges'),
    path('trust-badges/add/', views.TrustIndicatorCreateView.as_view(), name='trust_badge_add'),
    path('trust-badges/<int:pk>/edit/', views.TrustIndicatorUpdateView.as_view(), name='trust_badge_edit'),
    path('trust-badges/<int:pk>/delete/', views.TrustIndicatorDeleteView.as_view(), name='trust_badge_delete'),

    # Feature Cards Management
    path('feature-cards/', views.FeatureCardListView.as_view(), name='feature_cards'),
    path('feature-cards/add/', views.FeatureCardCreateView.as_view(), name='feature_card_create'),
    path('feature-cards/<int:pk>/edit/', views.FeatureCardUpdateView.as_view(), name='feature_card_edit'),
    path('feature-cards/<int:pk>/delete/', views.FeatureCardDeleteView.as_view(), name='feature_card_delete'),

    # Company Stats Management
    path('company-stats/', views.CompanyStatListView.as_view(), name='company_stats'),
    path('company-stats/add/', views.CompanyStatCreateView.as_view(), name='company_stat_create'),
    path('company-stats/<int:pk>/edit/', views.CompanyStatUpdateView.as_view(), name='company_stat_edit'),
    path('company-stats/<int:pk>/delete/', views.CompanyStatDeleteView.as_view(), name='company_stat_delete'),

    # Products Management
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/images/add/', views.product_image_add, name='product_image_add'),
    path('products/images/<int:pk>/delete/', views.ProductImageDeleteView.as_view(), name='product_image_delete'),
    path('products/images/<int:pk>/set-primary/', views.product_image_set_primary, name='product_image_set_primary'),

    # Categories Management
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # Inquiry Management - Contact Messages
    path('inquiries/contact-messages/', views.ContactMessageListView.as_view(), name='contact_messages'),
    path('inquiries/contact-messages/<int:pk>/', views.ContactMessageDetailView.as_view(), name='contact_message_detail'),
    path('inquiries/contact-messages/<int:pk>/delete/', views.ContactMessageDeleteView.as_view(), name='contact_message_delete'),
    path('inquiries/contact-messages/export/', views.export_contact_messages_csv, name='contact_messages_export'),

    # Inquiry Management - Quote Requests
    path('inquiries/quote-requests/', views.QuoteRequestListView.as_view(), name='quote_requests'),
    path('inquiries/quote-requests/<int:pk>/', views.QuoteRequestDetailView.as_view(), name='quote_request_detail'),
    path('inquiries/quote-requests/<int:pk>/delete/', views.QuoteRequestDeleteView.as_view(), name='quote_request_delete'),
    path('inquiries/quote-requests/export/', views.export_quote_requests_csv, name='quote_requests_export'),
]
