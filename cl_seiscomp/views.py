from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
import requests, openpyxl, datetime, os
from django.http import JsonResponse, HttpResponse
from core.models import Operator
from io import StringIO
from django.views import View
from django.shortcuts import redirect
from .models import CsRecord, StationListModel
from django.contrib import messages
import csv

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

class CsListView(ListView):
    model = CsRecord
    template_name = 'cl_seiscomp/cs_list.html'
    # context_object_name = 'csrecords'

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

# class QcRecordCreateView(CreateView):
#     model = QcRecord
#     form_class = QcRecordForm
#     template_name = 'cl_seiscomp/cs_form.html'
#     success_url = reverse_lazy('cl_seiscomp:csrecord_list')

# class QcRecordUpdateView(UpdateView):
#     model = QcRecord
#     form_class = QcRecordForm
#     template_name = 'cl_seiscomp/cs_form.html'
#     success_url = reverse_lazy('cl_seiscomp:csrecord_list')

# class QcRecordDeleteDirectView(View):
#     def post(self, request, pk, *args, **kwargs):
#         try:
#             record = QcRecord.objects.get(pk=pk)
#             record.delete()
#             return redirect('cl_seiscomp:csrecord_list')
#         except QcRecord.DoesNotExist:
#             return HttpResponse(status=404)