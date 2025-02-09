from django import forms
from .models import BastRecordModel

class BastRecordForm(forms.ModelForm):
    bast_id = forms.CharField()
    class Meta:
        model = BastRecordModel
        fields = '__all__'