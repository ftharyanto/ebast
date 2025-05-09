from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db.models import Count

class Command(BaseCommand):
    help = 'Find and display duplicate records for any model and field.'

    def add_arguments(self, parser):
        parser.add_argument('--app', type=str, required=True, help='App label (e.g., qc)')
        parser.add_argument('--model', type=str, required=True, help='Model name (e.g., ErrorStation)')
        parser.add_argument('--field', type=str, required=True, help='Field name to check for duplicates (e.g., kode_stasiun)')

    def handle(self, *args, **options):
        app_label = options['app']
        model_name = options['model']
        field_name = options['field']
        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            raise CommandError(f"Model {model_name} not found in app {app_label}.")
        if not hasattr(model, field_name):
            raise CommandError(f"Field {field_name} not found in model {model_name}.")
        duplicates = (
            model.objects
            .values(field_name)
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )
        if duplicates:
            self.stdout.write(self.style.WARNING(f'Duplicate {field_name} found in {model_name}:'))
            for dup in duplicates:
                self.stdout.write(f"{field_name}: {dup[field_name]} (Count: {dup['count']})")
                ids = model.objects.filter(**{field_name: dup[field_name]}).values_list('id', flat=True)
                self.stdout.write(f"  IDs: {list(ids)}")
        else:
            self.stdout.write(self.style.SUCCESS('No duplicates found.')) 