from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Dummy response for now
        bot_response = "You said: " + user_message

        return JsonResponse({'response': bot_response})

def home(request):
    return render(request, 'Niulize/base.html')
