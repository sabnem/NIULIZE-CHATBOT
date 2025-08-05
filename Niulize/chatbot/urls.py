from django.urls import path
from .views import chatbot_view, home

urlpatterns = [
    path('', home, name='home'),
    path('chatbot/', chatbot_view, name='chatbot'),
]
