"""Tests for the shorten app views."""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from shorten.models import long_urls


class IndexViewTest(TestCase):
    """Test cases for the index view."""
    
    def setUp(self):
        """Set up test client."""
        self.client = Client()
        self.index_url = reverse('index')
    
    def test_index_view_get_request(self):
        """Test that GET request to index returns the form."""
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_index_view_post_valid_url(self):
        """Test that POST request with valid URL creates a shortened URL."""
        response = self.client.post(self.index_url, {
            'long_url': 'https://www.example.com/very/long/url'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(long_urls.objects.count(), 1)
        
        url_entry = long_urls.objects.first()
        self.assertEqual(url_entry.long_url, 'https://www.example.com/very/long/url')
        self.assertIsNotNone(url_entry.short_code)
    
    def test_index_view_post_empty_url(self):
        """Test that POST request with empty URL shows error."""
        response = self.client.post(self.index_url, {
            'long_url': ''
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(long_urls.objects.count(), 0)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('error' in str(m) for m in messages))
    
    def test_index_view_duplicate_url(self):
        """Test that posting the same URL returns the existing shortened URL."""
        url_str = 'https://www.example.com/duplicate'
        
        # Create first URL
        response1 = self.client.post(self.index_url, {'long_url': url_str})
        self.assertEqual(long_urls.objects.count(), 1)
        
        # Post the same URL again
        response2 = self.client.post(self.index_url, {'long_url': url_str})
        self.assertEqual(long_urls.objects.count(), 1)


class LinksViewTest(TestCase):
    """Test cases for the links view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.links_url = reverse('links')
        
        # Create test URLs
        self.url1 = long_urls.objects.create(
            long_url='https://www.example1.com',
            short_code='abc123',
            clicks=5
        )
        self.url2 = long_urls.objects.create(
            long_url='https://www.example2.com',
            short_code='def456',
            clicks=10
        )
    
    def test_links_view_get_request(self):
        """Test that GET request to links displays all URLs."""
        response = self.client.get(self.links_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'links.html')
    
    def test_links_view_context(self):
        """Test that links view provides correct context data."""
        response = self.client.get(self.links_url)
        
        self.assertEqual(len(response.context['links']), 2)
        self.assertEqual(response.context['total_links'], 2)
        self.assertEqual(response.context['total_clicks'], 15)
    
    def test_links_view_ordering(self):
        """Test that links are ordered by creation date (newest first)."""
        response = self.client.get(self.links_url)
        links = response.context['links']
        
        self.assertEqual(links[0].id, self.url2.id)
        self.assertEqual(links[1].id, self.url1.id)


class RedirectViewTest(TestCase):
    """Test cases for the redirect view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.url = long_urls.objects.create(
            long_url='https://www.example.com',
            short_code='abc123'
        )
    
    def test_redirect_short_url(self):
        """Test that short URL redirects to original URL."""
        response = self.client.get(reverse('redirect_short', args=['abc123']))
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://www.example.com')
    
    def test_redirect_increments_clicks(self):
        """Test that redirect increments click count."""
        initial_clicks = self.url.clicks
        
        self.client.get(reverse('redirect_short', args=['abc123']))
        
        self.url.refresh_from_db()
        self.assertEqual(self.url.clicks, initial_clicks + 1)
    
    def test_redirect_invalid_short_code(self):
        """Test that invalid short code returns 404."""
        response = self.client.get(reverse('redirect_short', args=['invalid']))
        self.assertEqual(response.status_code, 404)


class DeleteViewTest(TestCase):
    """Test cases for the delete view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.url = long_urls.objects.create(
            long_url='https://www.example.com',
            short_code='abc123'
        )
    
    def test_delete_url(self):
        """Test that URL can be deleted."""
        response = self.client.get(reverse('delete_link', args=[self.url.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(long_urls.objects.count(), 0)
    
    def test_delete_invalid_url(self):
        """Test that deleting invalid URL returns 404."""
        response = self.client.get(reverse('delete_link', args=[999]))
        self.assertEqual(response.status_code, 404)
