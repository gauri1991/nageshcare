from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Inquiry
from .forms import InquiryForm


def submit_inquiry(request):
    """Handle product inquiry submissions (AJAX or regular form)"""
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()

            # Check if AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you! We will contact you soon about this product.'
                })
            else:
                messages.success(request, 'Thank you! We will contact you soon about this product.')
                return redirect('products:list')
        else:
            # Check if AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)

    return redirect('products:list')
