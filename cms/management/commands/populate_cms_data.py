"""
Management command to populate CMS with initial data
"""
from django.core.management.base import BaseCommand
from cms.models import (
    SiteSettings, HeroSection, FeatureCard, TrustIndicator,
    Testimonial, ClientIndustry, CompanyStat, TextContent,
    CallToAction
)


class Command(BaseCommand):
    help = 'Populates CMS with initial sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting CMS data population...'))

        # 1. Site Settings
        self.populate_site_settings()

        # 2. Hero Sections
        self.populate_hero_sections()

        # 3. Trust Indicators
        self.populate_trust_indicators()

        # 4. Text Content
        self.populate_text_content()

        # 5. Feature Cards
        self.populate_feature_cards()

        # 6. Testimonials
        self.populate_testimonials()

        # 7. Client Industries
        self.populate_client_industries()

        # 8. Company Stats
        self.populate_company_stats()

        # 9. Call to Actions
        self.populate_cta_sections()

        self.stdout.write(self.style.SUCCESS('✅ CMS data population completed successfully!'))

    def populate_site_settings(self):
        settings = SiteSettings.load()
        settings.business_name = 'NageshCare'
        settings.tagline = 'Your Trusted Partner for Quality Personal Care & Wellness Products'

        # Contact Information
        settings.phone_primary = '+91 98765 43210'
        settings.phone_whatsapp = '+91 98765 43210'
        settings.email_primary = 'info@nageshcare.com'
        settings.email_support = 'support@nageshcare.com'

        # Business Hours
        settings.business_hours = 'Mon-Fri: 9:00 AM - 6:00 PM, Sat: 9:00 AM - 2:00 PM'

        # Address
        settings.address_line1 = '123 Business Plaza, Trade District'
        settings.address_line2 = 'Near Commercial Complex'
        settings.city = 'Mumbai'
        settings.state = 'Maharashtra'
        settings.pincode = '400001'

        # Social Media
        settings.facebook_url = 'https://facebook.com/nageshcare'
        settings.linkedin_url = 'https://linkedin.com/company/nageshcare'
        settings.instagram_url = 'https://instagram.com/nageshcare'
        settings.whatsapp_url = 'https://wa.me/919876543210'

        # Business Details
        settings.gst_number = '27XXXXX0000X1Z5'
        settings.cin_number = 'U12345AB1234PLC123456'
        settings.established_year = '2010'

        # SEO
        settings.default_meta_description = 'Your trusted wholesale trading partner for premium personal care and wellness products. Quality bulk supplies with custom branding solutions.'
        settings.default_meta_keywords = 'wholesale tissue paper, bulk dhoop batti, personal care wholesale, white label products, trading company, bulk wellness products'

        settings.save()
        self.stdout.write('✓ Site Settings populated')

    def populate_hero_sections(self):
        heroes = [
            {
                'page_name': 'home',
                'title': 'Premium Bulk Trading Solutions for Your Business Growth',
                'subtitle': 'Your Trusted Partner for Quality Personal Care & Wellness Products at Wholesale Prices',
                'description': 'We specialize in bulk trading of premium white-label products. From scented tissue papers to authentic dhoop batti, we deliver quality at competitive prices.',
                'button1_text': 'Request a Quote',
                'button1_url': '/request-quote',
                'button2_text': 'View Our Products',
                'button2_url': '/products',
            },
            {
                'page_name': 'about',
                'title': 'Building Businesses Through Quality Trading',
                'subtitle': '',
                'description': 'At NageshCare, we believe that every successful retail business deserves a reliable wholesale partner. We are committed to bridging the gap between quality manufacturers and ambitious retailers.',
                'button1_text': 'Partner With Us',
                'button1_url': '/contact',
            },
            {
                'page_name': 'contact',
                'title': 'Get in Touch With Us',
                'subtitle': 'We\'re Here to Help Your Business Grow',
                'description': 'Have questions about our products, pricing, or bulk orders? Our team is ready to assist you. Whether you\'re a first-time buyer or a regular client, we\'re committed to providing prompt, helpful responses.',
            },
            {
                'page_name': 'products',
                'title': 'Quality Products at Wholesale Prices',
                'subtitle': 'Explore Our Carefully Curated Collection',
                'description': 'Browse our growing catalog of premium wholesale products. Each item is carefully selected, quality-tested, and available with custom branding options to help you build your business.',
                'button1_text': 'View All Products',
                'button1_url': '#products',
                'button2_text': 'Request Custom Sourcing',
                'button2_url': '/request-quote',
            },
        ]

        for hero_data in heroes:
            hero, created = HeroSection.objects.get_or_create(
                page_name=hero_data['page_name'],
                defaults=hero_data
            )
            if not created:
                for key, value in hero_data.items():
                    setattr(hero, key, value)
                hero.save()

        self.stdout.write('✓ Hero Sections populated')

    def populate_trust_indicators(self):
        indicators = [
            {
                'title': '100% Authentic',
                'subtitle': 'Verified Products',
                'icon_class': 'bi bi-shield-check',
                'position': 'hero',
                'order': 1,
            },
            {
                'title': 'Fast Delivery',
                'subtitle': 'Pan-India Shipping',
                'icon_class': 'bi bi-truck',
                'position': 'hero',
                'order': 2,
            },
            {
                'title': '24/7 Support',
                'subtitle': 'Always Available',
                'icon_class': 'bi bi-headset',
                'position': 'hero',
                'order': 3,
            },
            {
                'title': 'Secure Payments',
                'subtitle': 'Multiple Options',
                'icon_class': 'bi bi-lock',
                'position': 'hero',
                'order': 4,
            },
        ]

        for indicator_data in indicators:
            TrustIndicator.objects.get_or_create(
                title=indicator_data['title'],
                defaults=indicator_data
            )

        self.stdout.write('✓ Trust Indicators populated')

    def populate_text_content(self):
        text_contents = [
            {
                'page_name': 'home',
                'section_identifier': 'intro',
                'content_key': 'home-intro',
                'title': 'Wholesale Trading Made Simple',
                'content': 'Welcome to NageshCare, your dedicated wholesale trading partner for premium personal care and wellness products. We bridge the gap between manufacturers and retailers by sourcing, branding, and distributing high-quality products in bulk quantities.\n\nWhether you\'re a retailer, distributor, or business owner looking for reliable wholesale suppliers, we offer competitively priced products with flexible minimum order quantities. Our white-label solutions allow you to build your brand while we handle the supply chain complexities.',
            },
            {
                'page_name': 'about',
                'section_identifier': 'company-story',
                'content_key': 'about-company-story',
                'title': 'Our Journey',
                'content': 'NageshCare was founded with a simple yet powerful vision: to make premium products accessible to businesses of all sizes. We recognized that many retailers struggle to find trustworthy wholesale suppliers who offer both quality and affordability.\n\nStarting with personal care essentials like our premium scented tissue papers, we have built our reputation on three pillars: uncompromising quality, transparent pricing, and exceptional service. Today, we\'re expanding our product portfolio to include wellness products like authentic dhoop batti, always staying true to our commitment to excellence.\n\nWhat sets us apart is our unique approach to wholesale trading. We don\'t just move products from point A to point B. We invest time in understanding market trends, vetting manufacturers, and ensuring every product meets our stringent quality standards before it reaches you.',
            },
        ]

        for content_data in text_contents:
            TextContent.objects.get_or_create(
                content_key=content_data['content_key'],
                defaults=content_data
            )

        self.stdout.write('✓ Text Content populated')

    def populate_feature_cards(self):
        features = [
            # Why Choose Us - Home Page
            {
                'section_identifier': 'why-choose-us',
                'title': 'Quality Assurance',
                'description': 'Every product undergoes strict quality checks. We source only from certified manufacturers, ensuring you receive consistent, premium-quality products that enhance your brand reputation.',
                'icon_class': 'bi bi-award',
                'order': 1,
            },
            {
                'section_identifier': 'why-choose-us',
                'title': 'Competitive Wholesale Pricing',
                'description': 'Direct sourcing and efficient logistics mean better prices for you. We offer volume-based discounts and flexible payment terms to support your business cash flow.',
                'icon_class': 'bi bi-cash-coin',
                'order': 2,
            },
            {
                'section_identifier': 'why-choose-us',
                'title': 'White-Label Branding Options',
                'description': 'Build your brand identity with our customizable packaging solutions. We offer white-label services that let you put your brand front and center without the manufacturing hassle.',
                'icon_class': 'bi bi-badge-tm',
                'order': 3,
            },
            {
                'section_identifier': 'why-choose-us',
                'title': 'Reliable Supply Chain',
                'description': 'Never run out of stock. Our robust supply chain and inventory management ensure timely deliveries and consistent product availability for your business needs.',
                'icon_class': 'bi bi-truck',
                'order': 4,
            },
            {
                'section_identifier': 'why-choose-us',
                'title': 'Flexible Minimum Orders',
                'description': 'Whether you\'re a startup or an established retailer, we accommodate various order sizes. Scale your business at your own pace with our flexible MOQ policies.',
                'icon_class': 'bi bi-box-seam',
                'order': 5,
            },
            {
                'section_identifier': 'why-choose-us',
                'title': 'Dedicated Support',
                'description': 'Your success is our priority. Our responsive customer support team is always ready to assist with orders, inquiries, and business planning.',
                'icon_class': 'bi bi-headset',
                'order': 6,
            },

            # Vision & Mission - About Page
            {
                'section_identifier': 'about-vision-mission',
                'title': 'Our Vision',
                'description': 'To become the most trusted wholesale trading partner for personal care and wellness products across the region, empowering businesses to grow with quality, affordability, and reliability.',
                'icon_class': 'bi bi-eye',
                'order': 1,
            },
            {
                'section_identifier': 'about-vision-mission',
                'title': 'Our Mission',
                'description': 'We are committed to sourcing and supplying premium quality products at competitive wholesale prices, providing white-label branding solutions, maintaining a transparent and customer-centric approach, and supporting the growth of small and medium retailers.',
                'icon_class': 'bi bi-bullseye',
                'order': 2,
            },

            # How We Work - About Page
            {
                'section_identifier': 'how-we-work',
                'title': 'Strategic Sourcing',
                'description': 'We partner with certified manufacturers and conduct thorough quality assessments. Our sourcing team evaluates production facilities, raw material quality, and compliance standards.',
                'icon_class': 'bi bi-search',
                'order': 1,
            },
            {
                'section_identifier': 'how-we-work',
                'title': 'Quality Control',
                'description': 'Every product batch undergoes multi-level quality checks. From raw materials to finished goods, we maintain strict quality protocols that protect your business reputation.',
                'icon_class': 'bi bi-clipboard-check',
                'order': 2,
            },
            {
                'section_identifier': 'how-we-work',
                'title': 'White-Label Customization',
                'description': 'We offer flexible branding solutions. Whether you want minimal customization or full white-label packaging, we work with our manufacturing partners to bring your brand vision to life.',
                'icon_class': 'bi bi-palette',
                'order': 3,
            },
            {
                'section_identifier': 'how-we-work',
                'title': 'Efficient Distribution',
                'description': 'Our streamlined logistics ensure your orders reach you on time, every time. We maintain optimal inventory levels and work with reliable logistics partners.',
                'icon_class': 'bi bi-truck',
                'order': 4,
            },
            {
                'section_identifier': 'how-we-work',
                'title': 'Ongoing Support',
                'description': 'From your first inquiry to repeat orders, our team is with you every step. We provide market insights, product recommendations, and responsive customer service.',
                'icon_class': 'bi bi-headset',
                'order': 5,
            },

            # Values - About Page
            {
                'section_identifier': 'values',
                'title': 'Integrity',
                'description': 'Honesty and transparency guide every business decision we make. We believe in building long-term relationships based on trust and mutual respect.',
                'icon_class': 'bi bi-hand-thumbs-up',
                'order': 1,
            },
            {
                'section_identifier': 'values',
                'title': 'Quality First',
                'description': 'We never compromise on product quality. Every item in our catalog represents our commitment to excellence and our reputation in the market.',
                'icon_class': 'bi bi-star',
                'order': 2,
            },
            {
                'section_identifier': 'values',
                'title': 'Customer-Centricity',
                'description': 'Your success is our success. We go beyond transactional relationships to become genuine partners in your business growth.',
                'icon_class': 'bi bi-people',
                'order': 3,
            },
            {
                'section_identifier': 'values',
                'title': 'Innovation',
                'description': 'We continuously explore new products, better processes, and innovative solutions to stay ahead in the dynamic trading landscape.',
                'icon_class': 'bi bi-lightbulb',
                'order': 4,
            },
            {
                'section_identifier': 'values',
                'title': 'Sustainability',
                'description': 'We are committed to environmentally responsible practices, from sourcing eco-friendly products to minimizing packaging waste.',
                'icon_class': 'bi bi-tree',
                'order': 5,
            },
            {
                'section_identifier': 'values',
                'title': 'Fair Pricing',
                'description': 'We believe in value over volume. Our pricing structure ensures you get competitive rates without hidden costs or surprise charges.',
                'icon_class': 'bi bi-calculator',
                'order': 6,
            },
        ]

        for feature_data in features:
            FeatureCard.objects.get_or_create(
                section_identifier=feature_data['section_identifier'],
                title=feature_data['title'],
                defaults=feature_data
            )

        self.stdout.write('✓ Feature Cards populated')

    def populate_testimonials(self):
        testimonials = [
            {
                'customer_name': 'Rajesh Kumar',
                'customer_role': 'Retail Store Owner',
                'customer_location': 'Mumbai',
                'rating': 5,
                'testimonial_text': 'NageshCare has been our trusted partner for wholesale supplies for over 3 years. Their tissue paper quality and white-label branding service helped us build our own brand. Highly recommended!',
                'avatar_initials': 'RK',
                'is_featured': True,
                'order': 1,
            },
            {
                'customer_name': 'Priya Sharma',
                'customer_role': 'Hotel Manager',
                'customer_location': 'Taj Resort, Goa',
                'rating': 5,
                'testimonial_text': 'Excellent service and competitive bulk pricing. The scented tissue papers are a big hit with our guests. Their team is always responsive and delivers on time.',
                'avatar_initials': 'PS',
                'is_featured': True,
                'order': 2,
            },
            {
                'customer_name': 'Amit Patel',
                'customer_role': 'Distributor',
                'customer_location': 'Bangalore',
                'rating': 5,
                'testimonial_text': 'We have been working with NageshCare for 2 years. Their product range and flexible MOQ make them our go-to supplier for personal care products. Great partnership!',
                'avatar_initials': 'AP',
                'is_featured': True,
                'order': 3,
            },
            {
                'customer_name': 'Meera Reddy',
                'customer_role': 'Spa Owner',
                'customer_location': 'Serenity Spa, Hyderabad',
                'rating': 5,
                'testimonial_text': 'Professional team and premium quality products. The dhoop batti creates the perfect ambiance for our spa. NageshCare understands what businesses need.',
                'avatar_initials': 'MR',
                'is_featured': False,
                'order': 4,
            },
            {
                'customer_name': 'Suresh Gupta',
                'customer_role': 'E-commerce Seller',
                'customer_location': 'Pune',
                'rating': 5,
                'testimonial_text': 'Best wholesale rates in the market. Their white-label service helped me launch my own brand on Amazon. The ordering process is simple and delivery is always on time.',
                'avatar_initials': 'SG',
                'is_featured': False,
                'order': 5,
            },
        ]

        for testimonial_data in testimonials:
            Testimonial.objects.get_or_create(
                customer_name=testimonial_data['customer_name'],
                defaults=testimonial_data
            )

        self.stdout.write('✓ Testimonials populated')

    def populate_client_industries(self):
        industries = [
            {
                'industry_name': 'Retail Stores',
                'icon_class': 'bi bi-shop',
                'description': 'Supermarkets and retail outlets',
                'order': 1,
            },
            {
                'industry_name': 'Hotels & Resorts',
                'icon_class': 'bi bi-building',
                'description': 'Hospitality and accommodation businesses',
                'order': 2,
            },
            {
                'industry_name': 'Spas & Salons',
                'icon_class': 'bi bi-flower1',
                'description': 'Beauty and wellness centers',
                'order': 3,
            },
            {
                'industry_name': 'Yoga Studios',
                'icon_class': 'bi bi-person-arms-up',
                'description': 'Yoga and meditation centers',
                'order': 4,
            },
            {
                'industry_name': 'Temples & Ashrams',
                'icon_class': 'bi bi-star',
                'description': 'Spiritual and religious institutions',
                'order': 5,
            },
            {
                'industry_name': 'Distributors',
                'icon_class': 'bi bi-truck',
                'description': 'Wholesale distributors and traders',
                'order': 6,
            },
            {
                'industry_name': 'E-commerce Sellers',
                'icon_class': 'bi bi-cart',
                'description': 'Online retail businesses',
                'order': 7,
            },
            {
                'industry_name': 'Event Planners',
                'icon_class': 'bi bi-calendar-event',
                'description': 'Wedding and event management companies',
                'order': 8,
            },
        ]

        for industry_data in industries:
            ClientIndustry.objects.get_or_create(
                industry_name=industry_data['industry_name'],
                defaults=industry_data
            )

        self.stdout.write('✓ Client Industries populated')

    def populate_company_stats(self):
        stats = [
            {
                'section': 'home-testimonials',
                'label': 'Happy Clients',
                'value': '500+',
                'icon_class': 'bi bi-people',
                'order': 1,
            },
            {
                'section': 'home-testimonials',
                'label': 'Products',
                'value': '5000+',
                'icon_class': 'bi bi-box-seam',
                'order': 2,
            },
            {
                'section': 'home-testimonials',
                'label': 'Years Experience',
                'value': '15+',
                'icon_class': 'bi bi-calendar-check',
                'order': 3,
            },
            {
                'section': 'home-testimonials',
                'label': 'Cities Served',
                'value': '50+',
                'icon_class': 'bi bi-geo-alt',
                'order': 4,
            },
        ]

        for stat_data in stats:
            CompanyStat.objects.get_or_create(
                section=stat_data['section'],
                label=stat_data['label'],
                defaults=stat_data
            )

        self.stdout.write('✓ Company Stats populated')

    def populate_cta_sections(self):
        ctas = [
            {
                'page_name': 'home',
                'title': 'Ready to Grow Your Business?',
                'description': 'Join hundreds of satisfied retailers and distributors who trust NageshCare for their wholesale product needs. Let\'s discuss how we can support your business goals.',
                'primary_button_text': 'Request Bulk Quote',
                'primary_button_url': '/request-quote',
                'secondary_button_text': 'Contact Our Team',
                'secondary_button_url': '/contact',
            },
            {
                'page_name': 'about',
                'title': 'Partner With Us Today',
                'description': 'Whether you\'re launching a new retail venture or expanding your existing product line, we\'re here to support your journey. Let\'s discuss how NageshCare can become your trusted wholesale partner.',
                'primary_button_text': 'Start Your Business Journey',
                'primary_button_url': '/contact',
            },
            {
                'page_name': 'products',
                'title': 'Need a Custom Solution?',
                'description': 'Looking for products not listed in our catalog? We offer custom sourcing services for businesses with specific requirements. Contact our team to discuss your needs.',
                'primary_button_text': 'Request Custom Sourcing',
                'primary_button_url': '/request-quote',
                'secondary_button_text': 'Contact Our Team',
                'secondary_button_url': '/contact',
            },
        ]

        for cta_data in ctas:
            CallToAction.objects.get_or_create(
                page_name=cta_data['page_name'],
                defaults=cta_data
            )

        self.stdout.write('✓ Call to Action sections populated')
