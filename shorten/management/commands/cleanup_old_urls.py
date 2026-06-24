"""
Management command to clean up old or unused shortened URLs.

Usage:
    python manage.py cleanup_old_urls --days 365 --min-clicks 0
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from shorten.models import long_urls


class Command(BaseCommand):
    help = 'Clean up old or unused shortened URLs'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=365,
            help='Delete URLs not accessed for this many days (default: 365)'
        )
        parser.add_argument(
            '--min-clicks',
            type=int,
            default=0,
            help='Delete URLs with this many or fewer clicks (default: 0)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        min_clicks = options['min_clicks']
        dry_run = options['dry_run']
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        urls_to_delete = long_urls.objects.filter(
            created_at__lt=cutoff_date,
            clicks__lte=min_clicks
        )
        
        count = urls_to_delete.count()
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} URLs created before '
                    f'{cutoff_date} with {min_clicks} or fewer clicks'
                )
            )
            for url in urls_to_delete[:10]:
                self.stdout.write(f'  - {url.short_code}: {url.long_url}')
            if count > 10:
                self.stdout.write(f'  ... and {count - 10} more')
        else:
            urls_to_delete.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {count} URLs'
                )
            )
