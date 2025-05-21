from django import forms
from .models import BastRecordModel
from django.forms import DateInput

class BastRecordForm(forms.ModelForm):
    bast_id = forms.CharField()
    class Meta:
        model = BastRecordModel
        fields = '__all__'