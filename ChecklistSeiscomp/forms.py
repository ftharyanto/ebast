from django import forms
from .models import ChecklistSeiscompModel, OperatorModel, StationListModel

# creating a form
class InputForm(forms.ModelForm):
    operator = forms.ModelChoiceField(
        queryset=OperatorModel.objects.all().order_by('name'), initial=0)

    # create meta class
    class Meta:
        # specify model to be used
        model = ChecklistSeiscompModel

        # specify fields to be used
        fields = '__all__'

        widgets = {
            'gaps': forms.Textarea(attrs={
                'class': 'tooltipped',
                'data-position': 'bottom',
                'data-tooltip': 'masukan kode stasiun yang mengalami gap, pisahkan dengan baris baru (enter)',
                'placeholder': 'contoh: ABCD',
            }),
            'spikes': forms.Textarea(attrs={
                'class': 'tooltipped',
                'data-position': 'bottom',
                'data-tooltip': 'masukan kode stasiun yang mengalami spike, pisahkan dengan baris baru (enter)',
                'placeholder': 'contoh: ABCD',
            }),
            'blanks': forms.Textarea(attrs={
                'class': 'tooltipped',
                'data-position': 'bottom',
                'data-tooltip': 'masukan kode stasiun yang mengalami blank, pisahkan dengan baris baru (enter)',
                'placeholder': 'contoh: ABCD',
            }),
            'slmon': forms.NumberInput(attrs={
                'class': 'tooltipped',
                'data-position': 'bottom',
                'data-tooltip': 'Jumlah sensor yang delay lebih dari 30 menit',
                'placeholder': 'Contoh: 30',
            }),
            'tanggal': forms.TextInput(attrs={
                'class': 'datepicker',
                'name': 'tanggal',
                'placeholder': 'yyyy-mm-dd',

            })
        }


class OperatorForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = OperatorModel

        # specify fields to be used
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nama'}),
            'nip': forms.TextInput(attrs={'placeholder': 'NIP'}),
        }
        labels = {
            'name': ('Nama'),
            'nip': ('NIP'),
        }

class StationListForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = StationListModel

        # specify fields to be used
        fields = '__all__'
        widgets = {
            'kode': forms.TextInput(attrs={'placeholder': 'Kode Stasiun'}),
            'lokasi': forms.TextInput(attrs={'placeholder': 'Lokasi Stasiun'}),
            'tipe': forms.TextInput(attrs={'placeholder': 'Garansi atau Nongaransi'}),
        }
        labels = {
            'kode': ('Kode'),
            'stasiun': ('Lokasi Stasiun'),
            'tipe': ('Tipe Stasiun'),
        }
