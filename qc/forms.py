from django import forms
from .models import QcRecord

class QcRecordForm(forms.ModelForm):
    class Meta:
        model = QcRecord
        fields = ['qc_prev', 'qc', 'operator', 'qc_id', 'kelompok', 'jam_pelaksanaan', 'NIP']
