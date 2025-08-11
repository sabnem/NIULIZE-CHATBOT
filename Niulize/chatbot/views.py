from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FAQ, ChatLog
import json
import re

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def find_best_match(user_message):
    """Find the best matching FAQ response from database based on keywords"""
    user_message = user_message.lower().strip()
    
    # Remove common punctuation
    user_message = re.sub(r'[?!.,]', '', user_message)
    
    # Get all active FAQs ordered by priority
    faqs = FAQ.objects.filter(is_active=True).order_by('-priority', 'title')
    
    # Check for exact or partial matches with scoring
    best_match = None
    highest_score = 0
    matched_faq = None
    
    for faq in faqs:
        score = 0
        keywords = faq.get_keywords_list()
        
        for keyword in keywords:
            if keyword in user_message:
                # Give higher score for longer keyword matches
                score += len(keyword.split())
        
        if score > highest_score:
            highest_score = score
            best_match = faq.response
            matched_faq = faq
    
    # Return best match or default response
    if best_match:
        return best_match, matched_faq
    
    # Default response with suggestions
    default_response = """I'm sorry, I didn't understand your question. Here are some topics I can help with:

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
    
    return default_response, None

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
            
            # Find the best matching response from database
            bot_response, matched_faq = find_best_match(user_message)
            
            # Log the bot response (optional, for debugging)
            print(f"Bot answer: {bot_response[:50]}...")
            
            # Save chat log to database
            try:
                ChatLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    user_message=user_message,
                    bot_response=bot_response,
                    matched_faq=matched_faq,
                    ip_address=get_client_ip(request)
                )
            except Exception as log_error:
                print(f"Error saving chat log: {str(log_error)}")
                # Continue even if logging fails
            
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
    """Render the home page with chatbot interface"""
    return render(request, 'Niulize/home.html')

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'Niulize/login.html')

def register_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'Niulize/register.html', {'form': form})

def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')