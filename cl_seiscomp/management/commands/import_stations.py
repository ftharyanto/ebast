import csv
from django.core.management.base import BaseCommand
from cl_seiscomp.models import StationListModel

class Command(BaseCommand):
    help = 'Import station data from CSV file'

    def handle(self, *args, **options):
        # First, delete all existing station data
        StationListModel.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing station data cleared'))

        # Read and import new data
        with open('station_list.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Extract coordinates
                coordinates = row.get('Coordinates', '').strip()
                if coordinates:
                    try:
                        # Split by comma and take first two values (lat, lon)
                        lat, lon, _ = coordinates.split(',')
                        lat = float(lat)
                        lon = float(lon)
                    except (ValueError, IndexError):
                        lat = lon = None
                else:
                    lat = lon = None

                station = StationListModel(
                    network=row['network'],
                    code=row['code'],
                    province=row['province'],
                    location=row['location'],
                    digitizer_type=row['digitizer_type'],
                    UPT=row['UPT'],
                    longitude=lon,
                    latitude=lat,
                )
                station.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported station data'))
