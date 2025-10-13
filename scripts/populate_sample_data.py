#!/usr/bin/env python
"""
Populate sample data for NageshCare website
Run this script from the project root: python scripts/populate_sample_data.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')
django.setup()

from products.models import Category, Product, ProductImage, ProductVariant, FragranceOption


def create_categories():
    """Create product categories"""
    print("Creating categories...")

    categories = [
        {
            'name': 'Personal Care',
            'slug': 'personal-care',
            'description': 'Premium personal care products for retail and wholesale',
            'icon': 'bi-droplet'
        },
        {
            'name': 'Wellness & Spiritual',
            'slug': 'wellness-spiritual',
            'description': 'Authentic wellness and spiritual products',
            'icon': 'bi-flower1'
        }
    ]

    created_categories = []
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"  ✓ Created category: {category.name}")
        else:
            print(f"  - Category already exists: {category.name}")
        created_categories.append(category)

    return created_categories


def create_tissue_paper_product(category):
    """Create Premium Scented Tissue Paper product"""
    print("\nCreating Tissue Paper product...")

    product, created = Product.objects.get_or_create(
        slug='premium-scented-tissue-papers',
        defaults={
            'name': 'Premium Scented Tissue Papers',
            'category': category,
            'tagline': 'Luxury Softness with Long-Lasting Fragrance',
            'short_description': 'Soft, fragrant, and eco-friendly tissue papers available in bulk quantities. Perfect for retail stores, hotels, and hospitality businesses.',
            'full_description': '''Elevate your customers' experience with our premium scented tissue papers. Made from 100% virgin pulp and infused with carefully selected fragrances, these tissues combine superior softness with pleasant, long-lasting aromas.

Perfect for retail stores, hospitality businesses, hotels, spas, and commercial establishments looking to offer their customers a touch of luxury. Our white-label branding options allow you to build your own brand identity while we handle the product quality and supply chain.

Key Benefits:
• Ultra-soft texture that's gentle on skin
• Long-lasting fragrance without being overwhelming
• Sustainable sourcing and biodegradable materials
• Hygienic individually wrapped packs
• White-label ready for custom branding
• Dermatologically tested for all skin types''',
            'features': '''100% Virgin Pulp - Ultra-soft texture
Long-Lasting Fragrance - Carefully formulated scents
Eco-Friendly Production - Sustainable sourcing
Hygienic Packaging - Individually wrapped packs
White-Label Ready - Custom branding available
Dermatologically Tested - Safe for sensitive skin''',
            'minimum_order_quantity': '500 packs (negotiable for regular customers)',
            'is_featured': True,
            'is_active': True,
            'meta_title': 'Premium Scented Tissue Paper Wholesale | White Label Branding',
            'meta_description': 'Buy premium scented tissue papers in bulk. 100% virgin pulp, eco-friendly, custom white-label branding available. Ideal for retailers, hotels, and businesses.'
        }
    )

    if created:
        print(f"  ✓ Created product: {product.name}")

        # Create variants
        variants = [
            {
                'variant_name': 'Pocket Pack (100 Sheets)',
                'description': 'Ideal for retail stores and individual consumers. Compact size perfect for handbags and travel.'
            },
            {
                'variant_name': 'Family Pack (200 Sheets)',
                'description': 'Best for household use and small businesses. Economic value pack.'
            },
            {
                'variant_name': 'Bulk Box (500+ Sheets)',
                'description': 'Perfect for hotels, restaurants, and commercial use. Premium box packaging available.'
            }
        ]

        for variant_data in variants:
            ProductVariant.objects.create(product=product, **variant_data)
        print(f"  ✓ Created {len(variants)} variants")

        # Create fragrances
        fragrances = [
            {'name': 'Lavender Fresh', 'description': 'Calming lavender scent'},
            {'name': 'Rose Garden', 'description': 'Classic rose fragrance'},
            {'name': 'Ocean Breeze', 'description': 'Fresh oceanic aroma'},
            {'name': 'Citrus Burst', 'description': 'Energizing citrus notes'},
            {'name': 'Jasmine Bloom', 'description': 'Delicate jasmine essence'},
            {'name': 'Sandalwood Essence', 'description': 'Warm sandalwood aroma'}
        ]

        for frag_data in fragrances:
            FragranceOption.objects.create(product=product, **frag_data)
        print(f"  ✓ Created {len(fragrances)} fragrances")

    else:
        print(f"  - Product already exists: {product.name}")

    return product


def create_dhoop_batti_product(category):
    """Create Authentic Dhoop Batti product"""
    print("\nCreating Dhoop Batti product...")

    product, created = Product.objects.get_or_create(
        slug='authentic-dhoop-batti',
        defaults={
            'name': 'Authentic Dhoop Batti Incense Sticks',
            'category': category,
            'tagline': 'Sacred Aromas from Traditional Craftsmanship',
            'short_description': 'Handcrafted dhoop batti made from natural ingredients. Long-lasting fragrance for spiritual and aromatic purposes. Ideal for retail stores, temples, and wellness centers.',
            'full_description': '''Experience the essence of traditional Indian aromatherapy with our authentic dhoop batti incense sticks. Handcrafted using time-honored methods and natural ingredients, our dhoop batti offers long-lasting fragrance that creates a peaceful, spiritual atmosphere.

Ideal for retail stores, temples, yoga studios, meditation centers, spiritual shops, and wellness establishments. We offer bulk wholesale pricing and white-label packaging options to help you establish your own brand in the growing wellness market.

Made with 100% natural ingredients including herbs, resins, and essential oils. Each stick burns for 45-60 minutes providing consistent aroma release.''',
            'features': '''100% Natural Ingredients - Herbs, resins, aromatic compounds
Handcrafted Quality - Traditional preparation methods
Long-Lasting Fragrance - 45-60 minutes per stick
Charcoal-Free Options - Cleaner burning with minimal smoke
Spiritual & Therapeutic - Perfect for meditation and yoga
White-Label Ready - Custom packaging available
Eco-Friendly - Biodegradable materials''',
            'minimum_order_quantity': '1,000 sticks (minimum 50 packs of 20 sticks)',
            'is_featured': False,
            'is_coming_soon': True,
            'is_active': True,
            'meta_title': 'Wholesale Dhoop Batti Incense Sticks | Natural Ingredients | Bulk Orders',
            'meta_description': 'Premium dhoop batti incense sticks wholesale. Handcrafted from natural ingredients with long-lasting fragrance. Perfect for retailers, temples, spiritual stores.'
        }
    )

    if created:
        print(f"  ✓ Created product: {product.name}")

        # Create variants
        variants = [
            {
                'variant_name': 'Retail Pack (20 Sticks)',
                'description': 'Perfect for individual retail customers. Attractive retail-ready packaging.'
            },
            {
                'variant_name': 'Family Pack (40 Sticks)',
                'description': 'Best value for regular users. Suitable for yoga studios and small temples.'
            },
            {
                'variant_name': 'Bulk Pack (100 Sticks)',
                'description': 'For temples, ashrams, and meditation centers. Commercial establishments and distributors.'
            }
        ]

        for variant_data in variants:
            ProductVariant.objects.create(product=product, **variant_data)
        print(f"  ✓ Created {len(variants)} variants")

        # Create fragrances
        fragrances = [
            {'name': 'Sandalwood Supreme', 'description': 'Classic sandalwood for spiritual rituals'},
            {'name': 'Temple Rose', 'description': 'Traditional rose essence'},
            {'name': 'Mogra (Jasmine)', 'description': 'Pure jasmine for peaceful ambiance'},
            {'name': 'Sacred Loban', 'description': 'Benzoin resin for purification'},
            {'name': 'Lavender Calm', 'description': 'Relaxation and stress relief'},
            {'name': 'Nag Champa Classic', 'description': 'Popular aromatic blend'}
        ]

        for frag_data in fragrances:
            FragranceOption.objects.create(product=product, **frag_data)
        print(f"  ✓ Created {len(fragrances)} fragrances")

    else:
        print(f"  - Product already exists: {product.name}")

    return product


def main():
    """Main function to populate sample data"""
    print("=" * 60)
    print("NageshCare Sample Data Population Script")
    print("=" * 60)

    # Create categories
    categories = create_categories()
    personal_care = Category.objects.get(slug='personal-care')
    wellness = Category.objects.get(slug='wellness-spiritual')

    # Create products
    tissue_product = create_tissue_paper_product(personal_care)
    dhoop_product = create_dhoop_batti_product(wellness)

    print("\n" + "=" * 60)
    print("✓ Sample data population completed successfully!")
    print("=" * 60)
    print(f"\nCreated:")
    print(f"  • {Category.objects.count()} categories")
    print(f"  • {Product.objects.count()} products")
    print(f"  • {ProductVariant.objects.count()} product variants")
    print(f"  • {FragranceOption.objects.count()} fragrance options")
    print("\nYou can now:")
    print("  1. Access the admin panel to add product images")
    print("  2. View products at: http://localhost:8000/products/")
    print("  3. Add more products through the admin panel")


if __name__ == '__main__':
    main()
