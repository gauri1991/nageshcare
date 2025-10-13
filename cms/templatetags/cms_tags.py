"""
Template tags for accessing CMS data in frontend templates
"""
import logging
from django import template
from cms.models import (
    SiteSettings, HeroSection, FeatureCard, TrustIndicator,
    Testimonial, ClientIndustry, CompanyStat, TextContent,
    CallToAction
)

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def get_site_settings():
    """
    Get site-wide settings
    Usage: {% get_site_settings as settings %}
    """
    return SiteSettings.load()


@register.simple_tag
def get_hero(page_name):
    """
    Get hero section for a specific page
    Usage: {% get_hero 'home' as hero %}
    """
    try:
        return HeroSection.objects.get(page_name=page_name, is_active=True)
    except HeroSection.DoesNotExist:
        return None


@register.simple_tag
def get_trust_indicators(position='hero'):
    """
    Get trust indicators for a specific position
    Usage: {% get_trust_indicators 'hero' as trust_indicators %}
    """
    return TrustIndicator.objects.filter(position=position, is_active=True)


@register.simple_tag
def get_text_content(content_key):
    """
    Get text content by unique key
    Usage: {% get_text_content 'home-intro' as intro %}
    """
    try:
        return TextContent.objects.get(content_key=content_key, is_active=True)
    except TextContent.DoesNotExist:
        return None


@register.simple_tag
def get_feature_cards(section_identifier):
    """
    Get feature cards for a specific section
    Usage: {% get_feature_cards 'why-choose-us' as features %}
    """
    return FeatureCard.objects.filter(
        section_identifier=section_identifier,
        is_active=True
    )


@register.simple_tag
def get_testimonials(featured_only=False, limit=None):
    """
    Get testimonials, optionally filtered by featured status
    Usage: {% get_testimonials featured_only=True limit=3 as testimonials %}
    """
    testimonials = Testimonial.objects.filter(is_active=True)

    if featured_only:
        testimonials = testimonials.filter(is_featured=True)

    if limit:
        testimonials = testimonials[:limit]

    return testimonials


@register.simple_tag
def get_client_industries():
    """
    Get all active client industries
    Usage: {% get_client_industries as industries %}
    """
    return ClientIndustry.objects.filter(is_active=True)


@register.simple_tag
def get_company_stats(section='home-testimonials'):
    """
    Get company statistics for a specific section
    Usage: {% get_company_stats 'home-testimonials' as stats %}
    """
    return CompanyStat.objects.filter(section=section, is_active=True)


@register.simple_tag
def get_cta(page_name):
    """
    Get call-to-action for a specific page
    Usage: {% get_cta 'home' as cta %}
    """
    try:
        return CallToAction.objects.get(page_name=page_name, is_active=True)
    except CallToAction.DoesNotExist:
        return None


# Inclusion tags for complex components

@register.inclusion_tag('cms/components/hero.html')
def render_hero(page_name):
    """
    Render hero section for a page
    Usage: {% render_hero 'home' %}
    """
    try:
        hero = HeroSection.objects.get(page_name=page_name, is_active=True)
    except HeroSection.DoesNotExist:
        hero = None

    return {
        'hero': hero,
        'trust_indicators': TrustIndicator.objects.filter(position='hero', is_active=True)
    }


@register.inclusion_tag('cms/components/testimonials.html')
def render_testimonials(limit=3, featured_only=True):
    """
    Render testimonials section
    Usage: {% render_testimonials limit=3 featured_only=True %}
    """
    testimonials = Testimonial.objects.filter(is_active=True)

    if featured_only:
        testimonials = testimonials.filter(is_featured=True)

    if limit:
        testimonials = testimonials[:limit]

    return {
        'testimonials': testimonials,
        'stats': CompanyStat.objects.filter(section='home-testimonials', is_active=True)
    }


@register.inclusion_tag('cms/components/industries.html')
def render_industries():
    """
    Render client industries section
    Usage: {% render_industries %}
    """
    return {
        'industries': ClientIndustry.objects.filter(is_active=True)
    }


@register.inclusion_tag('cms/components/cta.html')
def render_cta(page_name):
    """
    Render call-to-action section
    Usage: {% render_cta 'home' %}
    """
    try:
        cta = CallToAction.objects.get(page_name=page_name, is_active=True)
    except CallToAction.DoesNotExist:
        cta = None

    return {
        'cta': cta
    }


# Filters

@register.filter
def stars_range(rating):
    """
    Returns a range for rendering star ratings
    Usage: {% for i in testimonial.rating|stars_range %}
    """
    return range(1, 6)


@register.filter
def is_star_filled(star_number, rating):
    """
    Check if a star should be filled
    Usage: {% if forloop.counter|is_star_filled:testimonial.rating %}
    """
    return star_number <= rating
