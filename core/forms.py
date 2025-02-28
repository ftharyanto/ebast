from django import forms
from .models import Operator, Kelompok

class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = '__all__'

class KelompokForm(forms.ModelForm):
    class Meta:
        model = Kelompok
        fields = '__all__'