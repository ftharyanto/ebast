from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import QcRecord
from .forms import QcRecordForm
from django.shortcuts import render
import requests, openpyxl, datetime, os
import pandas as pd
from django.http import JsonResponse, HttpResponse
from .models import Operator
from io import StringIO
from openpyxl.utils.dataframe import dataframe_to_rows

class QcRecordListView(ListView):
    model = QcRecord
    template_name = 'qc/qcrecord_list.html'
    context_object_name = 'qcrecords'

class QcRecordCreateView(CreateView):
    model = QcRecord
    form_class = QcRecordForm
    template_name = 'qc/qcrecord_form.html'
    success_url = reverse_lazy('qc:qcrecord_list')

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
    df_selected = df_selected[['Date', 'OT (UTC)', 'Lat', 'Long', 'Mag', 'TypeMag', 'D(Km)', 'Phase', 'RMS', 'Az. Gap', 'Region']]
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

def get_nip(request, operator_id):
    try:
        operator = Operator.objects.get(id=operator_id)
        return JsonResponse({'nip': operator.NIP})
    except Operator.DoesNotExist:
        return JsonResponse({'error': 'Operator not found'}, status=404)

def export_to_excel(request):
    records = QcRecord.objects.all()
    file_path = os.path.join(os.path.dirname(__file__), 'static/qc/QC Seiscomp.xlsx')
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    sheet.title = 'QC Records'

    for idx, record in enumerate(records, start=2):
        tanggal = format_date_indonesian(record.qc_id[:-2])
        hari = get_hari_indonesia(record.qc_id[:-2])
        sheet['G2'] = ': ' + tanggal
        sheet['G3'] = ': ' + hari
        sheet['G4'] = f': {record.jam_pelaksanaan.strftime("%H:%M")} - selesai'
        sheet['G5'] = f': {record.kelompok}'
        sheet['M18'] = tanggal
        sheet['M24'] = record.operator.name
        NIP = sheet['M25'] = 'NIP. ' + record.NIP

        # import the qc_prev and qc values from the record using pandas and fill the C8 to M8 row with the qc_prev and qc values alternatingly, add rows as needed
        qc_prev = pd.read_csv(StringIO(record.qc_prev))
        
        # add prev columns with 'prev' values to the last column
        qc_prev['prev'] = 'prev'

        # add rows to the sheet
        rows_to_add = len(qc_prev)
        sheet.insert_rows(8, amount=rows_to_add*2)
        qc_prev = dataframe_to_rows(qc_prev, index=False, header=False)

        qc = pd.read_csv(StringIO(record.qc))

        # add qc columns with 'QC' values to the last column
        qc['QC'] = 'QC'
        qc = dataframe_to_rows(qc, index=False, header=False)
        
        for r_idx, row in enumerate(qc_prev, 1):
            for c_idx, value in enumerate(row, 1):
                sheet.cell(row=r_idx*2+6, column=2, value=r_idx)
                sheet.cell(row=r_idx*2+6, column=c_idx+2, value=value)
                
        for r_idx, row in enumerate(qc, 1):
            for c_idx, value in enumerate(row, 1):
                sheet.cell(row=r_idx*2+7, column=c_idx+2, value=value)

    # Save the workbook to a BytesIO object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=qc_records.xlsx'    
    workbook.save(response)
    return response

import datetime

def format_date_indonesian(date_string):
    """Formats a date string in YYYY-MM-DD format into Indonesian date format.

    Args:
    date_string: The date string in YYYY-MM-DD format.

    Returns:
    The formatted date string in Indonesian format (DD MMMM YYYY).
    """

    date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d %B %Y")
    return formatted_date

def get_hari_indonesia(date_string):
    """
    Converts a date string (YYYY-MM-DD) to its corresponding Indonesian day name.

    Args:
        date_string: The date string in YYYY-MM-DD format.

    Returns:
        The Indonesian day name.
    """

    date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    hari_indonesia = date_obj.strftime("%A")
    hari_indonesia_map = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }
    return hari_indonesia_map[hari_indonesia]