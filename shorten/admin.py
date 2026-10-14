from django.contrib import admin
from django import forms

from .models import long_urls


class LongUrlsAdminForm(forms.ModelForm):
    class Meta:
        model = long_urls
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clicks'].required = False


@admin.register(long_urls)
class LongUrlsAdmin(admin.ModelAdmin):
    form = LongUrlsAdminForm
    list_display = ('short_code', 'long_url', 'clicks', 'created_at')
    search_fields = ('short_code', 'long_url')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
