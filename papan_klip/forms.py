from django import forms
from .models import PapanKlip

class PapanKlipForm(forms.ModelForm):
    class Meta:
        model = PapanKlip
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
