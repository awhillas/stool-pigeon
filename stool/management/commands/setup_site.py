from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Setup Site model for django-allauth'

    def handle(self, *args, **options):
        site, created = Site.objects.update_or_create(
            pk=1, 
            defaults={
                'domain': 'localhost:8000',
                'name': 'Stool Pigeon'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created site'))
        else:
            self.stdout.write(self.style.SUCCESS('Successfully updated site'))