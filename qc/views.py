from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import QcRecord
from .forms import QcRecordForm
from django.shortcuts import render
import requests
import pandas as pd
from django.http import JsonResponse

class QcRecordListView(ListView):
    model = QcRecord
    template_name = 'qc/qcrecord_list.html'
    context_object_name = 'qcrecords'

class QcRecordCreateView(CreateView):
    model = QcRecord
    form_class = QcRecordForm
    template_name = 'qc/qcrecord_form.html'
    success_url = reverse_lazy('qc:qcrecord_list')

    def form_valid(self, form):
        form.save()
        # update_excel_file(form.cleaned_data['tanggal'], form.cleaned_data['hari'], form.cleaned_data['jam'], form.cleaned_data['kelompok'], form.cleaned_data['operator'], form.cleaned_data['NIP'])
        return super().form_valid(form)

class QcRecordUpdateView(UpdateView):
    model = QcRecord
    form_class = QcRecordForm
    template_name = 'qc/qcrecord_form.html'
    success_url = reverse_lazy('qc:qcrecord_list')

class QcRecordDeleteView(DeleteView):
    model = QcRecord
    template_name = 'qc/qcrecord_confirm_delete.html'
    success_url = reverse_lazy('qc:qcrecord_list')


# Functions
def clean_index3(data, start_datetime='2024-12-11 13:00:00', end_datetime='2024-12-11 19:00:00'):
    text = data.decode('utf-8')

    lines = text.split('\n')
    processed_lines = []
    for i, line in enumerate(lines):
        if i not in [0, 1, 3]:
            line = '|'.join(part.strip() for part in line.split('|'))
            processed_lines.append(line)

    df = pd.DataFrame([x.split('|') for x in processed_lines[1:]], columns=processed_lines[0].split('|'))
    df['Origin Time (GMT)'] = pd.to_datetime(df['Origin Time (GMT)'], format='%Y-%m-%d %H:%M:%S')

    def select_data_by_datetime_range(df, start_datetime, end_datetime):
        mask = (df['Origin Time (GMT)'] >= start_datetime) & (df['Origin Time (GMT)'] <= end_datetime)
        return df.loc[mask]

    df_selected = select_data_by_datetime_range(df, start_datetime, end_datetime)

    # sort the df_selected by 'Origin Time (GMT)'
    df_selected = df_selected.sort_values(by='Origin Time (GMT)')

    # divide the 'Origin Time (GMT)' column into 'Date' and 'OT (UTC)' columns, and put them in the first two columns, remove the 'Origin Time (GMT)' column
    df_selected['Date'] = df_selected['Origin Time (GMT)'].dt.date
    df_selected['OT (UTC)'] = df_selected['Origin Time (GMT)'].dt.time
    df_selected = df_selected[['Date', 'OT (UTC)'] + [col for col in df_selected.columns if col != 'Origin Time (GMT)']]
    df_selected = df_selected.reset_index(drop=True)

    # sort the columns to be 'Date', 'OT (UTC)', 'Lat', 'Long', 'Mag', 'D(Km)', 'Phase', 'RMS', 'Az.Gap', 'Region', but first turn the respective column names into the desired ones
    df_selected = df_selected.rename(columns={'Lon': 'Long', 'Depth': 'D(Km)', 'cntP': 'Phase', 'AZgap': 'Az. Gap', 'Remarks': 'Region'})
    df_selected = df_selected[['Date', 'OT (UTC)', 'Lat', 'Long', 'Mag', 'D(Km)', 'Phase', 'RMS', 'Az. Gap', 'Region']]
    df_selected = df_selected.reset_index(drop=True)

    # Check for duplicate columns
    df_selected = df_selected.loc[:, ~df_selected.columns.duplicated()]
    
    return df_selected

def fetch_data(request, start_datetime='2024-12-11 13:00:00', end_datetime='2024-12-11 19:00:00'):
    url = "http://202.90.198.41/index3.txt"
    response = requests.get(url)

    if response.status_code == 200:
        data = clean_index3(response.content, start_datetime, end_datetime)
        csv_data = data.to_csv(index=False)
        return JsonResponse({'csv': csv_data})
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)

import openpyxl

def update_excel_file(tanggal, hari, jam, kelompok, operator, NIP):
    # Load the workbook and select the active worksheet
    workbook = openpyxl.load_workbook('QC Seiscomp.xlsx')
    sheet = workbook.active

    # Fill cell G2 with the specified value
    sheet['G2'] = ': ' + tanggal
    sheet['G3'] = ': ' + hari
    sheet['G4'] = f': {jam} - selesai'
    sheet['G5'] = f': {kelompok}'
    sheet['M18'] = tanggal
    sheet['M24'] = operator
    NIP = sheet['M25'] = 'NIP. ' + NIP

    # Save the workbook
    workbook.save('QC Seiscomp.xlsx')