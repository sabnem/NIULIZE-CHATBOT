from django.core.management.base import BaseCommand
from chatbot.models import FAQ, FAQCategory

class Command(BaseCommand):
    help = 'Populate the database with initial FAQ data'

    def handle(self, *args, **options):
        self.stdout.write('Populating FAQ database...')
        
        # Create categories
        categories_data = [
            {
                'name': 'General',
                'description': 'General greetings and information'
            },
            {
                'name': 'Services',
                'description': 'Information about our services'
            },
            {
                'name': 'Pricing',
                'description': 'Pricing and cost information'
            },
            {
                'name': 'Contact',
                'description': 'Contact and support information'
            },
            {
                'name': 'Company',
                'description': 'About our company and team'
            }
        ]
        
        for cat_data in categories_data:
            category, created = FAQCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Get categories
        general_cat = FAQCategory.objects.get(name='General')
        services_cat = FAQCategory.objects.get(name='Services')
        pricing_cat = FAQCategory.objects.get(name='Pricing')
        contact_cat = FAQCategory.objects.get(name='Contact')
        company_cat = FAQCategory.objects.get(name='Company')
        
        # Create FAQs
        faqs_data = [
            {
                'title': 'Greeting',
                'category': general_cat,
                'keywords': 'hello, hi, hey, good morning, good afternoon, good evening, greetings',
                'response': 'Hello! Welcome to Niulize. How can I help you today? You can ask me about our services, pricing, support, or contact information.',
                'priority': 10
            },
            {
                'title': 'Services Overview',
                'category': services_cat,
                'keywords': 'service, services, what do you do, what do you offer, products, web development, mobile app, digital marketing',
                'response': 'We offer comprehensive digital solutions:\n• Web Development (Custom websites, e-commerce)\n• Mobile App Development (iOS & Android)\n• Digital Marketing (SEO, Social Media, PPC)\n• UI/UX Design\n• Consulting Services\n\nWhich service interests you most?',
                'priority': 9
            },
            {
                'title': 'Web Development',
                'category': services_cat,
                'keywords': 'web development, website, web design, html, css, javascript, frontend, backend',
                'response': 'Our web development services include:\n• Custom website development\n• E-commerce solutions\n• Content Management Systems\n• Responsive design\n• Website maintenance\n\nWe use modern technologies like React, Django, and Node.js.',
                'priority': 8
            },
            {
                'title': 'Mobile App Development',
                'category': services_cat,
                'keywords': 'mobile app, app development, ios, android, mobile application',
                'response': 'We develop mobile applications for:\n• iOS (iPhone/iPad)\n• Android devices\n• Cross-platform solutions\n• App Store optimization\n• App maintenance and updates\n\nOur apps are built using React Native and native technologies.',
                'priority': 8
            },
            {
                'title': 'Pricing Information',
                'category': pricing_cat,
                'keywords': 'price, pricing, cost, how much, expensive, cheap, affordable, quote, estimate',
                'response': 'Our pricing structure:\n• Web Development: Starting from $2,000\n• Mobile Apps: Starting from $5,000\n• Digital Marketing: $500-2,000/month\n• Custom quotes available\n\nContact us for a detailed proposal tailored to your needs.',
                'priority': 9
            },
            {
                'title': 'Contact Information',
                'category': contact_cat,
                'keywords': 'contact, phone, email, address, reach you, get in touch',
                'response': 'Contact Information:\n📧 Email: info@niulize.com\n📞 Phone: +1-234-567-8900\n💬 WhatsApp: +1-234-567-8900\n📍 Address: 123 Business Street, City, State 12345\n🌐 Website: www.niulize.com',
                'priority': 9
            },
            {
                'title': 'Technical Support',
                'category': contact_cat,
                'keywords': 'support, help, problem, issue, bug, technical, assistance',
                'response': 'Technical Support:\n📧 Email: support@niulize.com\n📞 Hotline: +1-234-567-8901\n⏰ Hours: Monday-Friday, 9 AM - 6 PM\n🎫 Ticket System: Available on our website\n\nFor urgent issues, please call our hotline.',
                'priority': 8
            },
            {
                'title': 'Business Hours',
                'category': contact_cat,
                'keywords': 'hours, open, closed, working hours, business hours, when, schedule',
                'response': 'Business Hours:\n🕘 Monday - Friday: 9:00 AM - 6:00 PM\n🕙 Saturday: 10:00 AM - 4:00 PM\n🚫 Sunday: Closed\n\nFor after-hours support, please email us and we\'ll respond within 24 hours.',
                'priority': 7
            },
            {
                'title': 'Office Location',
                'category': contact_cat,
                'keywords': 'location, where, address, office, visit, directions',
                'response': 'Our Office Location:\n📍 123 Business Street, City, State 12345\n🚗 Parking available on-site\n🚇 Near Metro Station (Blue Line)\n\nVisitors welcome during business hours. Please schedule an appointment in advance.',
                'priority': 7
            },
            {
                'title': 'Our Team',
                'category': company_cat,
                'keywords': 'team, staff, developers, who, about us, company',
                'response': 'Our Team:\n• 15+ experienced developers\n• UI/UX designers\n• Project managers\n• Quality assurance specialists\n• Digital marketing experts\n\nWe\'re a passionate team dedicated to delivering exceptional digital solutions.',
                'priority': 6
            },
            {
                'title': 'Portfolio',
                'category': company_cat,
                'keywords': 'portfolio, work, projects, examples, showcase, case studies',
                'response': 'Our Portfolio:\n• 200+ websites delivered\n• 50+ mobile apps launched\n• Clients across 15+ industries\n• 99% client satisfaction rate\n\nVisit our website to see detailed case studies and client testimonials.',
                'priority': 6
            },
            {
                'title': 'Technologies',
                'category': services_cat,
                'keywords': 'technology, technologies, tech stack, programming, frameworks',
                'response': 'Technologies We Use:\n• Frontend: React, Vue.js, Angular\n• Backend: Python/Django, Node.js, PHP\n• Mobile: React Native, Flutter, Swift, Kotlin\n• Database: PostgreSQL, MongoDB, MySQL\n• Cloud: AWS, Azure, Google Cloud',
                'priority': 5
            }
        ]
        
        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                title=faq_data['title'],
                defaults={
                    'category': faq_data['category'],
                    'keywords': faq_data['keywords'],
                    'response': faq_data['response'],
                    'priority': faq_data['priority']
                }
            )
            if created:
                self.stdout.write(f'Created FAQ: {faq.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated FAQ database!')
        )
