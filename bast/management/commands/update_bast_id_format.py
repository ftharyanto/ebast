from django.core.management.base import BaseCommand
from bast.models import BastRecordModel
from qcfm.models import QcFmRecord
from qc.models import QcRecord
from cl_seiscomp.models import CsRecordModel

class Command(BaseCommand):
    help = 'Update ID format from old to new (e.g., 2025-05-01-P -> 2025-05-01-2P, etc.) for bast_id, qcfm_id, qc_id, cs_id.'

    def handle(self, *args, **options):
        suffix_map = {
            'D': '1D',
            'P': '2P',
            'S': '3S',
            'M': '4M',
        }
        updated = 0
        # Update bast_id
        for record in BastRecordModel.objects.all():
            if record.bast_id and len(record.bast_id) >= 2 and record.bast_id[-2] == '-':
                old_suffix = record.bast_id[-1]
                if old_suffix in suffix_map:
                    new_id = record.bast_id[:-1] + suffix_map[old_suffix]
                    self.stdout.write(f'Updating bast_id {record.bast_id} -> {new_id}')
                    record.bast_id = new_id
                    record.save()
                    updated += 1
        # Update qcfm_id
        for record in QcFmRecord.objects.all():
            if record.qcfm_id and len(record.qcfm_id) >= 2 and record.qcfm_id[-2] == '-':
                old_suffix = record.qcfm_id[-1]
                if old_suffix in suffix_map:
                    new_id = record.qcfm_id[:-1] + suffix_map[old_suffix]
                    self.stdout.write(f'Updating qcfm_id {record.qcfm_id} -> {new_id}')
                    record.qcfm_id = new_id
                    record.save()
                    updated += 1
        # Update qc_id
        for record in QcRecord.objects.all():
            if record.qc_id and len(record.qc_id) >= 2 and record.qc_id[-2] == '-':
                old_suffix = record.qc_id[-1]
                if old_suffix in suffix_map:
                    new_id = record.qc_id[:-1] + suffix_map[old_suffix]
                    self.stdout.write(f'Updating qc_id {record.qc_id} -> {new_id}')
                    record.qc_id = new_id
                    record.save()
                    updated += 1
        # Update cs_id
        for record in CsRecordModel.objects.all():
            if record.cs_id and len(record.cs_id) >= 2 and record.cs_id[-2] == '-':
                old_suffix = record.cs_id[-1]
                if old_suffix in suffix_map:
                    new_id = record.cs_id[:-1] + suffix_map[old_suffix]
                    self.stdout.write(f'Updating cs_id {record.cs_id} -> {new_id}')
                    record.cs_id = new_id
                    try:
                        record.save()
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Warning: Could not save cs_id {record.cs_id}: {e}'))
                    else:
                        updated += 1
        self.stdout.write(self.style.SUCCESS(f'Updated {updated} records across all apps.')) 