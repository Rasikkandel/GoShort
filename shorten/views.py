from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Sum, Avg
from django.urls import reverse
import string
import random
from .models import long_urls

BASE62 = string.digits + string.ascii_letters

def base62_encode(num):
    """Convert a number to base62"""
    if num == 0:
        return BASE62[0]
    
    result = []
    while num > 0:
        remainder = num % 62
        result.append(BASE62[remainder])
        num //= 62
    
    return ''.join(reversed(result))

def generate_short_code(length=6):
    """Generate a random short code"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@require_http_methods(["GET", "POST"])
def index(request):
    """Home page - Display form and shortening result"""
    shortened_url = None
    short_url = None
    
    if request.method == 'POST':
        long_url = request.POST.get('long_url', '').strip()
        
        if not long_url:
            messages.error(request, 'Please enter a URL')
        else:
            try:
                # Check if URL already exists
                existing = long_urls.objects.filter(long_url=long_url).first()
                if existing:
                    shortened_url = existing
                else:
                    # Generate unique short code
                    while True:
                        short_code = generate_short_code()
                        if not long_urls.objects.filter(short_code=short_code).exists():
                            break
                    
                    shortened_url = long_urls.objects.create(
                        long_url=long_url,
                        short_code=short_code
                    )
                
                # Build the short URL
                short_url = request.build_absolute_uri(reverse('redirect_short', kwargs={'short_code': shortened_url.short_code}))
                messages.success(request, 'URL shortened successfully!')
            except Exception as e:
                messages.error(request, f'Error creating short URL: {str(e)}')
    
    context = {
        'shortened_url': shortened_url,
        'short_url': short_url,
    }
    return render(request, 'index.html', context)

@require_http_methods(["GET"])
def links(request):
    """Display all shortened links with statistics"""
    links = long_urls.objects.all().order_by('-created_at')
    
    total_links = links.count()
    total_clicks = links.aggregate(total=Sum('clicks'))['total'] or 0
    avg_clicks = links.aggregate(avg=Avg('clicks'))['avg'] or 0
    
    context = {
        'links': links,
        'total_links': total_links,
        'total_clicks': total_clicks,
        'avg_clicks': avg_clicks,
    }
    return render(request, 'links.html', context)

@require_http_methods(["GET"])
def redirect_short(request, short_code):
    """Redirect short URL to original URL"""
    url_entry = get_object_or_404(long_urls, short_code=short_code)
    url_entry.clicks += 1
    url_entry.save()
    return redirect(url_entry.long_url)

@require_http_methods(["GET", "POST"])
def delete_link(request, link_id):
    """Delete a shortened URL"""
    url_entry = get_object_or_404(long_urls, id=link_id)
    url_entry.delete()
    messages.success(request, 'Link deleted successfully!')
    return redirect('links') 
