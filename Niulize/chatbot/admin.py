from django.contrib import admin
from .models import FAQ, FAQCategory, ChatLog

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'faq_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    
    def faq_count(self, obj):
        return obj.faqs.count()
    faq_count.short_description = 'Number of FAQs'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_active', 'priority', 'created_at']
    list_filter = ['category', 'is_active', 'priority', 'created_at']
    search_fields = ['title', 'keywords', 'response']
    list_editable = ['is_active', 'priority']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'is_active', 'priority')
        }),
        ('Content', {
            'fields': ('keywords', 'response'),
            'description': 'Keywords should be comma-separated (e.g., "hello, hi, greeting")'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user_message_preview', 'matched_faq', 'ip_address']
    list_filter = ['timestamp', 'matched_faq__category']
    search_fields = ['user_message', 'bot_response']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def user_message_preview(self, obj):
        return obj.user_message[:50] + "..." if len(obj.user_message) > 50 else obj.user_message
    user_message_preview.short_description = 'User Message'
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation of chat logs
