from django.core.management.base import BaseCommand
from qc.models import ErrorStation
from django.db.models import Count

class Command(BaseCommand):
    help = 'Find and display duplicate ErrorStation records by kode_stasiun.'

    def handle(self, *args, **options):
        duplicates = (
            ErrorStation.objects
            .values('kode_stasiun')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )
        if duplicates:
            self.stdout.write(self.style.WARNING('Duplicate Kode Stasiun found:'))
            for dup in duplicates:
                self.stdout.write(f"Kode Stasiun: {dup['kode_stasiun']} (Count: {dup['count']})")
                ids = ErrorStation.objects.filter(kode_stasiun=dup['kode_stasiun']).values_list('id', flat=True)
                self.stdout.write(f"  IDs: {list(ids)}")
        else:
            self.stdout.write(self.style.SUCCESS('No duplicates found.')) 