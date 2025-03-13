from django import forms
from .models import QcRecord

class QcRecordForm(forms.ModelForm):
    qc_id = forms.CharField()
    class Meta:
        model = QcRecord
        fields = '__all__'