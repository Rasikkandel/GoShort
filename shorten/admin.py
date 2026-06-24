from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum
from .models import long_urls


@admin.register(long_urls)
class LongUrlsAdmin(admin.ModelAdmin):
    """Enhanced admin interface for managing shortened URLs"""
    
    list_display = [
        'short_code_badge',
        'long_url_preview',
        'clicks_display',
        'created_at_display',
        'status_badge',
    ]
    
    list_filter = ['created_at', 'clicks']
    search_fields = ['short_code', 'long_url']
    readonly_fields = ['short_code', 'created_at', 'clicks', 'stats_summary']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('URL Information', {
            'fields': ('short_code', 'long_url')
        }),
        ('Statistics', {
            'fields': ('clicks', 'created_at', 'stats_summary')
        }),
    )
    
    actions = ['reset_clicks']
    
    def short_code_badge(self, obj):
        """Display short code as a colored badge"""
        url = reverse('admin:shorten_long_urls_change', args=[obj.pk])
        return format_html(
            '<a href="{}" style="'
            'display: inline-block; '
            'background-color: #4F46E5; '
            'color: white; '
            'padding: 6px 12px; '
            'border-radius: 6px; '
            'font-weight: 600; '
            'text-decoration: none;">{}</a>',
            url,
            obj.short_code
        )
    short_code_badge.short_description = 'Short Code'
    
    def long_url_preview(self, obj):
        """Display truncated URL with full text on hover"""
        return format_html(
            '<span title="{}" style="cursor: help;">{}</span>',
            obj.long_url,
            obj.long_url[:50] + '...' if len(obj.long_url) > 50 else obj.long_url
        )
    long_url_preview.short_description = 'Original URL'
    
    def clicks_display(self, obj):
        """Display clicks with a colored indicator"""
        if obj.clicks == 0:
            color = '#9CA3AF'
            label = 'No clicks'
        elif obj.clicks < 10:
            color = '#FCD34D'
            label = f'{obj.clicks} clicks'
        else:
            color = '#10B981'
            label = f'{obj.clicks} clicks'
        
        return format_html(
            '<span style="'
            'display: inline-block; '
            'background-color: {}; '
            'color: white; '
            'padding: 4px 8px; '
            'border-radius: 4px; '
            'font-size: 12px; '
            'font-weight: 600;">{}</span>',
            color,
            label
        )
    clicks_display.short_description = 'Clicks'
    
    def created_at_display(self, obj):
        """Display creation date in a readable format"""
        return obj.created_at.strftime('%b %d, %Y %H:%M')
    created_at_display.short_description = 'Created'
    
    def status_badge(self, obj):
        """Display URL status"""
        if obj.clicks > 100:
            status = 'Popular'
            color = '#10B981'
        elif obj.clicks > 10:
            status = 'Active'
            color = '#3B82F6'
        else:
            status = 'New'
            color = '#8B5CF6'
        
        return format_html(
            '<span style="'
            'display: inline-block; '
            'background-color: {}; '
            'color: white; '
            'padding: 4px 8px; '
            'border-radius: 4px; '
            'font-size: 12px; '
            'font-weight: 600;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Status'
    
    def stats_summary(self, obj):
        """Display comprehensive statistics"""
        total_urls = long_urls.objects.count()
        total_clicks = long_urls.objects.aggregate(Sum('clicks'))['clicks__sum'] or 0
        avg_clicks = total_clicks / total_urls if total_urls > 0 else 0
        
        return format_html(
            '<div style="background-color: #F3F4F6; padding: 15px; border-radius: 6px; font-size: 14px;">'
            '<p><strong>Total Shortened URLs:</strong> {}</p>'
            '<p><strong>Total Clicks (All URLs):</strong> {}</p>'
            '<p><strong>Average Clicks per URL:</strong> {:.2f}</p>'
            '<p><strong>This URL Clicks:</strong> {}</p>'
            '</div>',
            total_urls,
            total_clicks,
            avg_clicks,
            obj.clicks
        )
    stats_summary.short_description = 'Statistics Summary'
    
    def reset_clicks(self, request, queryset):
        """Action to reset clicks for selected URLs"""
        updated = queryset.update(clicks=0)
        self.message_user(
            request,
            f'{updated} URL(s) click count reset successfully.'
        )
    reset_clicks.short_description = 'Reset clicks for selected URLs'
    
    def has_delete_permission(self, request):
        """Allow deletion of URLs"""
        return True


# Customize admin site
admin.site.site_header = 'GoShort Administration'
admin.site.site_title = 'GoShort Admin'
admin.site.index_title = 'Welcome to GoShort Admin Dashboard'