from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class FAQCategory(models.Model):
    """Categories for organizing FAQ items"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class FAQ(models.Model):
    """Frequently Asked Questions with keyword-based matching"""
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    title = models.CharField(max_length=200, help_text="Brief title for this FAQ")
    keywords = models.TextField(
        help_text="Comma-separated keywords that trigger this response (e.g., 'hello, hi, greeting')"
    )
    response = models.TextField(help_text="The response to send when keywords match")
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(
        default=1, 
        help_text="Higher numbers have higher priority when multiple FAQs match"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-priority', 'title']
    
    def __str__(self):
        return self.title
    
    def get_keywords_list(self):
        """Return keywords as a list"""
        return [keyword.strip().lower() for keyword in self.keywords.split(',') if keyword.strip()]

class ChatLog(models.Model):
    """Log of chat interactions for analytics"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    matched_faq = models.ForeignKey(FAQ, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Chat Log"
        verbose_name_plural = "Chat Logs"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Chat at {self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.user_message[:50]}..."
