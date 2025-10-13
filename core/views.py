from django.shortcuts import render, redirect
from django.contrib import messages
from inquiries.models import ContactMessage, QuoteRequest
from inquiries.forms import ContactForm, QuoteRequestForm
from products.models import Product


def home(request):
    """Home page view"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]
    context = {
        'featured_products': featured_products,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page view"""
    return render(request, 'core/about.html')


def contact(request):
    """Contact page view with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('core:contact')
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'core/contact.html', context)


def request_quote(request):
    """Request quote page view with detailed form"""
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save()
            messages.success(
                request,
                f'Quote request submitted successfully! Your reference ID is: {quote.reference_id}. '
                'We will contact you within 24-48 hours.'
            )
            return redirect('core:home')
    else:
        form = QuoteRequestForm()

    context = {'form': form}
    return render(request, 'core/request_quote.html', context)
