"""Tests for the shorten app admin interface."""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from shorten.models import long_urls

User = get_user_model()


class AdminInterfaceTest(TestCase):
    """Test cases for the admin interface."""
    
    def setUp(self):
        """Set up test data and client."""
        self.client = Client()
        
        # Create superuser
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        # Create test URLs
        self.url1 = long_urls.objects.create(
            long_url='https://www.example1.com',
            short_code='abc123',
            clicks=0
        )
        self.url2 = long_urls.objects.create(
            long_url='https://www.example2.com',
            short_code='def456',
            clicks=50
        )
    
    def test_admin_login(self):
        """Test that admin can login."""
        logged_in = self.client.login(username='admin', password='admin123')
        self.assertTrue(logged_in)
    
    def test_admin_change_list(self):
        """Test that admin can view change list."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('admin:shorten_long_urls_changelist'))
        
        self.assertEqual(response.status_code, 200)
    
    def test_admin_add_url(self):
        """Test that admin can add URL through admin interface."""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.post(reverse('admin:shorten_long_urls_add'), {
            'long_url': 'https://www.newexample.com',
            'short_code': 'ghi789'
        })
        
        self.assertEqual(long_urls.objects.count(), 3)
    
    def test_admin_change_url(self):
        """Test that admin can change URL."""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.post(
            reverse('admin:shorten_long_urls_change', args=[self.url1.id]),
            {
                'long_url': 'https://www.updated.com',
                'short_code': self.url1.short_code,
                'clicks': 10
            }
        )
        
        self.url1.refresh_from_db()
        self.assertEqual(self.url1.long_url, 'https://www.updated.com')
    
    def test_admin_delete_url(self):
        """Test that admin can delete URL."""
        self.client.login(username='admin', password='admin123')
        
        self.client.post(
            reverse('admin:shorten_long_urls_delete', args=[self.url1.id]),
            {'post': 'yes'}
        )
        
        self.assertEqual(long_urls.objects.count(), 1)
