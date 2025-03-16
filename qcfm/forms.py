from django import forms
from .models import QcFmRecord

class QcFmRecordForm(forms.ModelForm):
    qcfm_id = forms.CharField()
    class Meta:
        model = QcFmRecord
        fields = '__all__'