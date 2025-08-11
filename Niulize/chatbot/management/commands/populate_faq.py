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
                'title': 'What is Niulize Chat?',
                'category': general_cat,
                'keywords': 'what is niulize, about, introduction, chatbot, AI, who are you, what do you do',
                'response': 'Hello! I am Niulize Chat, an AI assistant designed to help you with information about our services and support. I can answer questions about our services, pricing, technical support, and more. How can I assist you today?',
                'priority': 100
            },
            {
                'title': 'Our Services',
                'category': services_cat,
                'keywords': 'services, offerings, what services, solutions, products, development, consulting',
                'response': '🚀 We offer comprehensive digital solutions:\n\n💻 Web Development\n• Custom websites and web applications\n• E-commerce solutions\n• Progressive Web Apps (PWA)\n\n📱 Mobile Development\n• iOS and Android apps\n• Cross-platform solutions\n• App maintenance\n\n🤖 AI & Machine Learning\n• Custom AI solutions\n• Chatbots & Virtual Assistants\n• Data Analytics\n\n🎨 Design Services\n• UI/UX Design\n• Brand Identity\n• User Research\n\nWhich service would you like to know more about?',
                'priority': 95
            },
            {
                'title': 'Technology Stack',
                'category': services_cat,
                'keywords': 'technology, tech stack, programming languages, frameworks, tools, software',
                'response': '🛠️ Our Technology Stack:\n\n📚 Frontend\n• React.js / Next.js\n• Vue.js / Nuxt.js\n• TypeScript\n\n⚙️ Backend\n• Python / Django\n• Node.js / Express\n• Java Spring Boot\n\n📱 Mobile\n• React Native\n• Flutter\n• Swift & Kotlin\n\n🗄️ Databases\n• PostgreSQL\n• MongoDB\n• Redis\n\n☁️ Cloud\n• AWS\n• Google Cloud\n• Azure',
                'priority': 90
            },
            {
                'title': 'Pricing and Packages',
                'category': pricing_cat,
                'keywords': 'price, cost, rates, packages, how much, pricing, payment, fees',
                'response': '💰 Our Pricing Options:\n\n🎯 Project-Based\n• Web Apps: From $5,000\n• Mobile Apps: From $10,000\n• Custom Solutions: Based on requirements\n\n⏱️ Time & Materials\n• Senior Developer: $80-100/hour\n• Mid-level Developer: $60-80/hour\n• Designer: $70-90/hour\n\n🤝 Retainer Packages\n• Basic: $2,000/month\n• Professional: $5,000/month\n• Enterprise: Custom\n\n💡 All packages include:\n• Regular Updates\n• Technical Support\n• Documentation\n\nContact us for a detailed quote!',
                'priority': 85
            },
            {
                'title': 'Contact and Support',
                'category': contact_cat,
                'keywords': 'contact, reach, support, help, assistance, phone, email, office',
                'response': '📞 Contact Information:\n\n📧 Email\n• General: hello@niulize.com\n• Support: support@niulize.com\n\n☎️ Phone\n• Main: +254 700 000000\n• Support: +254 700 000001\n\n⏰ Business Hours\n• Monday-Friday: 8am-6pm EAT\n• Weekend Support: Emergency only\n\n📍 Location\n• Nairobi, Kenya\n• Remote teams worldwide\n\n💬 Live Chat\n• Available 24/7 through our website',
                'priority': 80
            },
            {
                'title': 'Development Process',
                'category': services_cat,
                'keywords': 'process, development, how it works, steps, methodology, timeline',
                'response': '🔄 Our Development Process:\n\n1. 📋 Discovery & Planning\n• Requirements gathering\n• Technical analysis\n• Project roadmap\n\n2. 🎨 Design\n• UI/UX design\n• Prototyping\n• Design review\n\n3. 🛠️ Development\n• Agile methodology\n• Regular updates\n• Quality assurance\n\n4. 🚀 Deployment\n• Testing\n• Launch\n• Monitoring\n\n5. � Maintenance\n• Regular updates\n• Performance monitoring\n• Security patches\n\nTypical Timeline: 2-6 months depending on project scope.',
                'priority': 75
            },
            {
                'title': 'Support Plans',
                'category': contact_cat,
                'keywords': 'support plans, maintenance, service level, response time, technical support',
                'response': '🛡️ Support & Maintenance Plans:\n\n🌟 Standard Support\n• Response time: 24 hours\n• Email support\n• Bug fixes\n• $500/month\n\n💎 Premium Support\n• Response time: 4 hours\n• Priority email & phone\n• Bug fixes & updates\n• Monthly reports\n• $1,000/month\n\n👑 Enterprise Support\n• Response time: 1 hour\n• 24/7 dedicated support\n• Custom SLA\n• Contact for pricing',
                'priority': 70
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
