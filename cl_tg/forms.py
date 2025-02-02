from django import forms
from .models import StationListModel

class StationListForm(forms.ModelForm):
    class Meta:
        model = StationListModel
        fields = '__all__'
