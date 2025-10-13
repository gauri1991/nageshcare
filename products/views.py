from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def product_list(request):
    """Product listing page with filters"""
    # Always load ALL products for client-side filtering
    all_products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')

    # Get category slug from URL (for initial state, not for filtering)
    category_slug = request.GET.get('category')

    # Search filter (still server-side for search functionality)
    search_query = request.GET.get('q')
    if search_query:
        all_products = all_products.filter(
            Q(name__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(full_description__icontains=search_query)
        )

    # Get all categories for filter buttons
    categories = Category.objects.all()

    context = {
        'products': all_products,  # Always send ALL products to template
        'categories': categories,
        'current_category': category_slug,  # Only for setting initial button state
        'search_query': search_query,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(
        Product.objects.prefetch_related('images', 'variants', 'fragrances'),
        slug=slug,
        is_active=True
    )

    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)
