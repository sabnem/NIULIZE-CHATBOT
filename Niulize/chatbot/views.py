from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import re
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
    try:
        user_message = user_message.lower().strip()
        
        # Remove common punctuation
        user_message = re.sub(r'[?!.,]', '', user_message)
        
        # Get all active FAQs ordered by priority
        faqs = FAQ.objects.filter(is_active=True).order_by('-priority', 'title')
        
        if not faqs.exists():
            return "I apologize, but my FAQ database is currently empty. Please contact the administrator.", None
        
        # Check for exact or partial matches with scoring
        best_match = None
        highest_score = 0
        matched_faq = None
        
        # Split user message into words for better matching
        user_words = set(user_message.split())
        
        for faq in faqs:
            score = 0
            keywords = faq.get_keywords_list()
            
            # Check exact phrase match
            if user_message in faq.title.lower() or user_message in faq.response.lower():
                score += 10
            
            # Check keyword matches
            for keyword in keywords:
                keyword = keyword.lower().strip()
                if keyword in user_message:
                    score += 3 * len(keyword.split())  # Weight longer phrases more heavily
                
                # Check individual word matches
                keyword_words = set(keyword.split())
                matching_words = user_words.intersection(keyword_words)
                score += len(matching_words)
            
            if score > highest_score:
                highest_score = score
                best_match = faq.response
                matched_faq = faq
        
        # Return best match if score is above threshold
        if highest_score >= 1:
            return best_match, matched_faq
        
        # Default response with suggestions
        suggestions = "\n".join([f"• {faq.title}" for faq in faqs[:5]])
        default_response = f"""I'm not quite sure what you're asking. Here are some topics I can help with:

{suggestions}

Please try asking about one of these topics or rephrase your question."""
        
        return default_response, None

    except Exception as e:
        print(f"Error in find_best_match: {str(e)}")
        return "I apologize, but I encountered an error. Please try again.", None

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
            try:
                bot_response, matched_faq = find_best_match(user_message)
                if not bot_response:
                    raise ValueError("No response generated")
                
                # Log the bot response (optional, for debugging)
                print(f"User question: {user_message}")
                print(f"Bot answer: {bot_response[:100]}...")
                
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
            except Exception as match_error:
                print(f"Error finding match: {str(match_error)}")
                raise
            
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