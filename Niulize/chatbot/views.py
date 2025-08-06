from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re

# Predefined FAQ responses with improved matching
FAQ_RESPONSES = {
    'greeting': {
        'keywords': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings'],
        'response': 'Hello! Welcome to Niulize. How can I help you today? You can ask me about our services, pricing, support, or contact information.'
    },
    'services': {
        'keywords': ['service', 'services', 'what do you do', 'what do you offer', 'products', 'web development', 'mobile app', 'digital marketing'],
        'response': 'We offer comprehensive digital solutions:\n• Web Development (Custom websites, e-commerce)\n• Mobile App Development (iOS & Android)\n• Digital Marketing (SEO, Social Media, PPC)\n• UI/UX Design\n• Consulting Services\n\nWhich service interests you most?'
    },
    'web_development': {
        'keywords': ['web development', 'website', 'web design', 'html', 'css', 'javascript', 'frontend', 'backend'],
        'response': 'Our web development services include:\n• Custom website development\n• E-commerce solutions\n• Content Management Systems\n• Responsive design\n• Website maintenance\n\nWe use modern technologies like React, Django, and Node.js.'
    },
    'mobile_app': {
        'keywords': ['mobile app', 'app development', 'ios', 'android', 'mobile application'],
        'response': 'We develop mobile applications for:\n• iOS (iPhone/iPad)\n• Android devices\n• Cross-platform solutions\n• App Store optimization\n• App maintenance and updates\n\nOur apps are built using React Native and native technologies.'
    },
    'pricing': {
        'keywords': ['price', 'pricing', 'cost', 'how much', 'expensive', 'cheap', 'affordable', 'quote', 'estimate'],
        'response': 'Our pricing structure:\n• Web Development: Starting from $2,000\n• Mobile Apps: Starting from $5,000\n• Digital Marketing: $500-2,000/month\n• Custom quotes available\n\nContact us for a detailed proposal tailored to your needs.'
    },
    'contact': {
        'keywords': ['contact', 'phone', 'email', 'address', 'reach you', 'get in touch'],
        'response': 'Contact Information:\n📧 Email: info@niulize.com\n📞 Phone: +1-234-567-8900\n💬 WhatsApp: +1-234-567-8900\n📍 Address: 123 Business Street, City, State 12345\n🌐 Website: www.niulize.com'
    },
    'support': {
        'keywords': ['support', 'help', 'problem', 'issue', 'bug', 'technical', 'assistance'],
        'response': 'Technical Support:\n📧 Email: support@niulize.com\n📞 Hotline: +1-234-567-8901\n⏰ Hours: Monday-Friday, 9 AM - 6 PM\n🎫 Ticket System: Available on our website\n\nFor urgent issues, please call our hotline.'
    },
    'hours': {
        'keywords': ['hours', 'open', 'closed', 'working hours', 'business hours', 'when', 'schedule'],
        'response': 'Business Hours:\n🕘 Monday - Friday: 9:00 AM - 6:00 PM\n🕙 Saturday: 10:00 AM - 4:00 PM\n🚫 Sunday: Closed\n\nFor after-hours support, please email us and we\'ll respond within 24 hours.'
    },
    'location': {
        'keywords': ['location', 'where', 'address', 'office', 'visit', 'directions'],
        'response': 'Our Office Location:\n📍 123 Business Street, City, State 12345\n🚗 Parking available on-site\n🚇 Near Metro Station (Blue Line)\n\nVisitors welcome during business hours. Please schedule an appointment in advance.'
    },
    'team': {
        'keywords': ['team', 'staff', 'developers', 'who', 'about us', 'company'],
        'response': 'Our Team:\n• 15+ experienced developers\n• UI/UX designers\n• Project managers\n• Quality assurance specialists\n• Digital marketing experts\n\nWe\'re a passionate team dedicated to delivering exceptional digital solutions.'
    },
    'portfolio': {
        'keywords': ['portfolio', 'work', 'projects', 'examples', 'showcase', 'case studies'],
        'response': 'Our Portfolio:\n• 200+ websites delivered\n• 50+ mobile apps launched\n• Clients across 15+ industries\n• 99% client satisfaction rate\n\nVisit our website to see detailed case studies and client testimonials.'
    },
    'technologies': {
        'keywords': ['technology', 'technologies', 'tech stack', 'programming', 'frameworks'],
        'response': 'Technologies We Use:\n• Frontend: React, Vue.js, Angular\n• Backend: Python/Django, Node.js, PHP\n• Mobile: React Native, Flutter, Swift, Kotlin\n• Database: PostgreSQL, MongoDB, MySQL\n• Cloud: AWS, Azure, Google Cloud'
    }
}

def find_best_match(user_message):
    """Find the best matching FAQ response based on keywords"""
    user_message = user_message.lower().strip()
    
    # Remove common punctuation
    user_message = re.sub(r'[?!.,]', '', user_message)
    
    # Check for exact or partial matches with scoring
    best_match = None
    highest_score = 0
    
    for category, faq in FAQ_RESPONSES.items():
        score = 0
        for keyword in faq['keywords']:
            if keyword in user_message:
                # Give higher score for longer keyword matches
                score += len(keyword.split())
        
        if score > highest_score:
            highest_score = score
            best_match = faq['response']
    
    # Return best match or default response
    if best_match:
        return best_match
    
    # Default response with suggestions
    return """I'm sorry, I didn't understand your question. Here are some topics I can help with:

🏢 **Company Information:**
• About our team and company
• Our portfolio and case studies

💼 **Services:**
• Web development
• Mobile app development
• Digital marketing

💰 **Business:**
• Pricing and quotes
• Technologies we use

📞 **Contact & Support:**
• Contact information
• Business hours and location
• Technical support

Please try asking about one of these topics, or rephrase your question."""

@csrf_exempt
def chatbot_view(request):
    """Handle chatbot requests and return appropriate responses"""
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            # Validate input
            if not user_message:
                return JsonResponse({
                    'response': 'Please enter a message to get started!',
                    'status': 'error'
                })
            
            # Log the user message (optional, for debugging)
            print(f"User question: {user_message}")
            
            # Find the best matching response
            bot_response = find_best_match(user_message)
            
            # Log the bot response (optional, for debugging)
            print(f"Bot answer: {bot_response[:50]}...")
            
            return JsonResponse({
                'response': bot_response,
                'status': 'success'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'response': 'Invalid message format. Please try again.',
                'status': 'error'
            }, status=400)
        except Exception as e:
            print(f"Error in chatbot_view: {str(e)}")
            return JsonResponse({
                'response': 'An error occurred. Please try again later.',
                'status': 'error'
            }, status=500)
    
    # Handle non-POST requests
    return JsonResponse({
        'response': 'Please use POST method to send messages.',
        'status': 'error'
    }, status=405)

def home(request):
    #Render the home page with chatbot interface
    return render(request, 'Niulize/base.html')