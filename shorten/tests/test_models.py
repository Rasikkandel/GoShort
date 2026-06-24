"""Tests for the shorten app models."""

from django.test import TestCase
from django.utils import timezone
from shorten.models import long_urls


class LongUrlsModelTest(TestCase):
    """Test cases for the long_urls model."""
    
    def setUp(self):
        """Set up test data."""
        self.url = long_urls.objects.create(
            long_url='https://www.example.com/very/long/url/path',
            short_code='abc123'
        )
    
    def test_url_creation(self):
        """Test that a URL can be created with required fields."""
        self.assertEqual(self.url.long_url, 'https://www.example.com/very/long/url/path')
        self.assertEqual(self.url.short_code, 'abc123')
        self.assertEqual(self.url.clicks, 0)
    
    def test_url_creation_timestamp(self):
        """Test that created_at is automatically set."""
        self.assertIsNotNone(self.url.created_at)
        self.assertLess(self.url.created_at, timezone.now())
    
    def test_short_code_is_unique(self):
        """Test that short_code must be unique."""
        with self.assertRaises(Exception):
            long_urls.objects.create(
                long_url='https://www.different-url.com',
                short_code='abc123'  # Duplicate
            )
    
    def test_url_string_representation(self):
        """Test the string representation of URL model."""
        expected_str = 'abc123 -> https://www.example.com/very/long/url/path'
        self.assertEqual(str(self.url), expected_str)
    
    def test_clicks_increment(self):
        """Test that clicks can be incremented."""
        initial_clicks = self.url.clicks
        self.url.clicks += 1
        self.url.save()
        
        self.url.refresh_from_db()
        self.assertEqual(self.url.clicks, initial_clicks + 1)
    
    def test_url_ordering(self):
        """Test that URLs are ordered by creation date (newest first)."""
        self.url2 = long_urls.objects.create(
            long_url='https://www.other-url.com',
            short_code='def456'
        )
        
        urls = long_urls.objects.all()
        self.assertEqual(urls[0].id, self.url2.id)
        self.assertEqual(urls[1].id, self.url.id)
