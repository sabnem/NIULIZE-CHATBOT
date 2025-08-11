from django.urls import path
from .views import chatbot_view, home, login_view, register_view, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('chatbot/', chatbot_view, name='chatbot'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
