from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
import requests, openpyxl, datetime, os
from django.http import JsonResponse, HttpResponse
from core.models import Operator
from io import StringIO
from django.views import View
from django.shortcuts import redirect
from .models import CsRecordModel, StationListModel
from django.contrib import messages
import csv

##### Station List Views
class StationListView(ListView):
    model = StationListModel
    template_name = 'cl_seiscomp/station_list.html'
    context_object_name = 'station_list'

class StationCreateView(CreateView):
    model = StationListModel
    template_name = 'cl_seiscomp/sl_form.html'
    fields = '__all__'
    success_url = reverse_lazy('cl_seiscomp:station_list')

class StationUpdateView(UpdateView):
    model = StationListModel
    template_name = 'cl_seiscomp/sl_form.html'
    fields = '__all__'
    success_url = reverse_lazy('cl_seiscomp:station_list')

class StationDeleteView(DeleteView):
    model = StationListModel
    template_name = 'cl_seiscomp/sl_confirm_delete.html'
    success_url = reverse_lazy('cl_seiscomp:station_list')

class StationBulkCreateView(View):
    template_name = 'cl_seiscomp/sl_bulk_create.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        csv_data = request.POST.get('csv_data')

        if not csv_file and not csv_data:
            messages.error(request, 'Please upload a CSV file or provide CSV data')
            return redirect('cl_seiscomp:sl_bulk_create')

        if csv_file:
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is not a CSV file')
                return redirect('cl_seiscomp:sl_bulk_create')

            file_data = csv_file.read().decode('utf-8')
            csv_reader = csv.reader(StringIO(file_data), delimiter=',')
            header = next(csv_reader)  # Skip the header row
        else:
            csv_reader = csv.reader(StringIO(csv_data), delimiter=',')

        for row in csv_reader:
            StationListModel.objects.create(
                network=row[0],
                code=row[1],
                province=row[2],
                location=row[3],
                digitizer_type=row[4],
                UPT=row[5]
            )

        messages.success(request, 'Stations added successfully')
        return redirect('cl_seiscomp:station_list')


##### Checklist Seiscomp View
class CsListView(ListView):
    model = CsRecordModel
    template_name = 'cl_seiscomp/cs_list.html'
    context_object_name = 'csrecords'

class CsCreateView(CreateView):
    model = CsRecordModel
    template_name = 'cl_seiscomp/cs_form.html'
    fields = '__all__'
    success_url = reverse_lazy('cl_seiscomp:cs_list')

    def form_valid(self, form):
        form.instance.slmon_image = self.request.FILES.get('slmon_image')
        return super().form_valid(form)

class CsUpdateView(UpdateView):
    model = CsRecordModel
    template_name = 'cl_seiscomp/cs_form.html'
    fields = '__all__'
    success_url = reverse_lazy('cl_seiscomp:cs_list')

    def form_valid(self, form):
        form.instance.slmon_image = self.request.FILES.get('slmon_image')
        return super().form_valid(form)

class CsDeleteView(DeleteView):
    model = CsRecordModel
    template_name = 'cl_seiscomp/cs_confirm_delete.html'
    success_url = reverse_lazy('cl_seiscomp:cs_list')

def cs_export_excel(request, record_id):
    from qc.views import format_date_indonesian, get_hari_indonesia
    import ast

    try:
        record = CsRecordModel.objects.get(id=record_id)
    except CsRecordModel.DoesNotExist:
        return HttpResponse(status=404)

    file_path = os.path.join(os.path.dirname(__file__), 'static/cl_seiscomp/cl_Seiscomp.xlsx')
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    sheet.title = 'Checklist Seiscomp'
    
    # tanggal = format_date_indonesian(record.cs_id[2:-2])
    # hari = get_hari_indonesia(record.cs_id[2:-2])
    sheet['A3'] = f'KELOMPOK: {record.kelompok}'
    sheet['A2'] = f'SHIFT {record.shift.upper()}'
    sheet['H266'] = f'{record.operator}'
    jam_pelaksanaan = f'JAM {record.jam_pelaksanaan}'
    sheet['D5'], sheet['P5'], sheet['H253'] = jam_pelaksanaan, jam_pelaksanaan, jam_pelaksanaan

    gaps = ast.literal_eval(record.gaps)
    spikes = ast.literal_eval(record.spikes)
    blanks = ast.literal_eval(record.blanks)

    # for cells B7:B269
    for row in range(7, 269+1):  # Iterate through rows 7 to 269
        cell_value = sheet.cell(row=row, column=2).value  # Get the cell value in column B

        if cell_value in gaps:
            sheet.cell(row=row, column=4).value = 1
        if cell_value in spikes:
            sheet.cell(row=row, column=5).value = 1
        if cell_value in blanks:
            sheet.cell(row=row, column=6).value = 1

    # for cells I7:I250
    for row in range(7, 250+1):  # Iterate through rows 7 to 269
        cell_value = sheet.cell(row=row, column=9).value  # Get the cell value in column B

        if cell_value in gaps:
            sheet.cell(row=row, column=16).value = 1
        if cell_value in spikes:
            sheet.cell(row=row, column=17).value = 1
        if cell_value in blanks:
            sheet.cell(row=row, column=18).value = 1

    # Save the workbook to a BytesIO object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=CS-{record.cs_id}.xlsx'
    workbook.save(response)

    return response