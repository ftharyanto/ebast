from django import forms
from django.core.exceptions import ValidationError
from .models import PapanKlip
import os

class PapanKlipForm(forms.ModelForm):
    class Meta:
        model = PapanKlip
        fields = ['title', 'content', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        if file:
            # Limit file size to 5MB
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("File size must be under 5MB")
            
            # Validate file extensions
            valid_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.jpg', '.jpeg', '.png', '.txt']
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError('Unsupported file type. Please upload a document or image file.')
        
        return file
