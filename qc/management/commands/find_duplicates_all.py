from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Count, CharField, IntegerField, TextField
from django.db.models.fields import DateField, DateTimeField, TimeField

class Command(BaseCommand):
    help = 'Find and display duplicate records for all models using the first user-input field. Optionally delete duplicates.'

    def handle(self, *args, **options):
        skip_apps = {'admin', 'auth', 'contenttypes', 'sessions'}
        for model in apps.get_models():
            model_name = model.__name__
            app_label = model._meta.app_label
            # Skip StationListModel in cl_seiscomp app
            if app_label == 'cl_seiscomp' and model_name == 'StationListModel':
                continue
            # Skip Django built-in apps
            if app_label in skip_apps:
                continue
            # Find the first user-input field (CharField, IntegerField, or TextField), not pk, not date/time
            user_fields = [
                f for f in model._meta.fields
                if not f.primary_key and not isinstance(f, (DateField, DateTimeField, TimeField))
                and isinstance(f, (CharField, IntegerField, TextField))
            ]
            if not user_fields:
                continue
            field = user_fields[0].name
            duplicates = (
                model.objects
                .values(field)
                .annotate(count=Count(field))
                .filter(count__gt=1)
            )
            if duplicates:
                self.stdout.write(self.style.WARNING(f'[{app_label}.{model_name}] Duplicate {field}:'))
                for dup in duplicates:
                    self.stdout.write(f"  {field}: {dup[field]} (Count: {dup['count']})")
                    ids = list(model.objects.filter(**{field: dup[field]}).values_list('pk', flat=True))
                    self.stdout.write(f"    PKs: {ids}")
                # Prompt for deletion
                confirm = input(f"Delete duplicates for [{app_label}.{model_name}] field '{field}'? (y/N): ").strip().lower()
                if confirm == 'y':
                    for dup in duplicates:
                        records = list(model.objects.filter(**{field: dup[field]}).order_by('pk'))
                        # Keep the first, delete the rest
                        to_delete = records[1:]
                        deleted_pks = [obj.pk for obj in to_delete]
                        for obj in to_delete:
                            obj.delete()
                        if deleted_pks:
                            self.stdout.write(self.style.ERROR(f"    Deleted PKs: {deleted_pks}"))
                        else:
                            self.stdout.write("    Nothing deleted (only one record present).")
            else:
                self.stdout.write(self.style.SUCCESS(f'[{app_label}.{model_name}] No duplicates found for field {field}.')) 