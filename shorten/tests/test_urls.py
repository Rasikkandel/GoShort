"""Tests for the shorten app URL routing."""

from django.test import TestCase
from django.urls import reverse, resolve
from shorten import views


class UrlResolutionTest(TestCase):
    """Test cases for URL resolution."""
    
    def test_index_url_resolves(self):
        """Test that index URL resolves to the index view."""
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)
    
    def test_links_url_resolves(self):
        """Test that links URL resolves to the links view."""
        url = reverse('links')
        self.assertEqual(resolve(url).func, views.links)
    
    def test_redirect_short_url_resolves(self):
        """Test that short URL redirect resolves to the redirect view."""
        url = reverse('redirect_short', args=['abc123'])
        self.assertEqual(resolve(url).func, views.redirect_short)
    
    def test_delete_link_url_resolves(self):
        """Test that delete URL resolves to the delete view."""
        url = reverse('delete_link', args=[1])
        self.assertEqual(resolve(url).func, views.delete_link)
