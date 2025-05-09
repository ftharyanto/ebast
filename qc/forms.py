from django import forms
from .models import QcRecord, ErrorStation
from cl_seiscomp.models import StationListModel

class QcRecordForm(forms.ModelForm):
    qc_id = forms.CharField()
    class Meta:
        model = QcRecord
        fields = '__all__'
        # fields = ['qc_prev', 'qc', 'operator', 'qc_id', 'kelompok', 'jam_pelaksanaan', 'NIP']

class ErrorStationForm(forms.ModelForm):
    kode_stasiun = forms.ChoiceField(choices=[], label='Kode Stasiun')
    lokasi = forms.CharField(label='Lokasi', required=False)

    class Meta:
        model = ErrorStation
        fields = ['kode_stasiun', 'lokasi', 'deskripsi_error']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kode_stasiun'].choices = [('', '--- Pilih Kode Stasiun ---')] + [
            (s.code, s.code) for s in StationListModel.objects.all()
        ]
        if self.instance and self.instance.kode_stasiun:
            # Optionally pre-fill lokasi if editing
            try:
                s = StationListModel.objects.get(code=self.instance.kode_stasiun)
                self.fields['lokasi'].initial = f"{s.province} - {s.location} - {s.UPT}"
            except StationListModel.DoesNotExist:
                pass
