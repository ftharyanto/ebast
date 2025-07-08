from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Operator, Kelompok
from django.urls import reverse_lazy
from .forms import OperatorForm, KelompokForm
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import csv

class HomeView(TemplateView):
    template_name = 'core/homepage.html'

class OperatorListView(ListView):
    model = Operator
    template_name = 'core/operator_list.html'
    context_object_name = 'operator'

class OperatorCreateView(CreateView):
    model = Operator
    form_class = OperatorForm
    template_name = 'core/operator_form.html'
    success_url = reverse_lazy('core:operator_list')

class OperatorUpdateView(UpdateView):
    model = Operator
    form_class = OperatorForm
    template_name = 'core/operator_form.html'
    success_url = reverse_lazy('core:operator_list')

class OperatorDeleteDirectView(View):
    def post(self, request, pk, *args, **kwargs):
        try:
            record = Operator.objects.get(pk=pk)
            record.delete()
            return redirect('core:operator_list')
        except Operator.DoesNotExist:
            return HttpResponse(status=404)

class OperatorBulkCreateView(View):
    template_name = 'core/operator_bulk_create.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        csv_data = request.POST.get('csv_data')

        if csv_file:
            if not csv_file.name.endswith('.csv'):
                return HttpResponse('File is not CSV type', status=400)
            file_data = csv_file.read().decode('utf-8')
        elif csv_data:
            file_data = csv_data
        else:
            return HttpResponse('No CSV file or data provided', status=400)

        reader = csv.reader(file_data.splitlines())
        for row in reader:
            if len(row) >= 2:
                Operator.objects.create(name=row[0], NIP=row[1])

        return redirect('core:operator_list')

def get_operator_list(request):
    operators = Operator.objects.values('pk', 'name')
    return JsonResponse({'operators': list(operators)})

def health_check(request):
    """Health check endpoint for Docker container monitoring"""
    return JsonResponse({'status': 'healthy', 'service': 'ebast'})

class KelompokListView(ListView):
    model = Kelompok
    template_name = 'core/kelompok_list.html'
    context_object_name = 'kelompok'

class KelompokCreateView(CreateView):
    model = Kelompok
    form_class = KelompokForm
    template_name = 'core/kelompok_form.html'
    success_url = reverse_lazy('core:kelompok_list')

class KelompokUpdateView(UpdateView):
    model = Kelompok
    form_class = KelompokForm
    template_name = 'core/kelompok_form.html'
    success_url = reverse_lazy('core:kelompok_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing_members'] = self.object.member.split(',')
        return context

class KelompokDeleteDirectView(View):
    def post(self, request, pk, *args, **kwargs):
        try:
            record = Kelompok.objects.get(pk=pk)
            record.delete()
            return redirect('core:kelompok_list')
        except Kelompok.DoesNotExist:
            return HttpResponse(status=404)
