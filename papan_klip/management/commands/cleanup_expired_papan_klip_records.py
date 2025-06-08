from django.core.management.base import BaseCommand
from django.utils import timezone
from papan_klip.models import PapanKlip

class Command(BaseCommand):
    help = 'Deletes PapanKlip entries that have expired'

    def handle(self, *args, **options):
        # Get current time
        now = timezone.now()
        
        # Find and delete expired entries
        expired_count = PapanKlip.objects.filter(expires_at__lte=now).count()
        if expired_count > 0:
            self.stdout.write(f'Deleting {expired_count} expired PapanKlip entries...')
            deleted_count, _ = PapanKlip.objects.filter(expires_at__lte=now).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} expired PapanKlip entries'))
        else:
            self.stdout.write('No expired PapanKlip entries to delete')
