from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import PapanKlip
from .forms import PapanKlipForm

# API Views
def papan_klip_list_api(request):
    from django.utils import timezone
    from django.db import connection
    import json
    
    try:
        now = timezone.now()
        
        # Get non-expired records
        records = PapanKlip.objects.filter(expires_at__gt=now).order_by('-created_at')
        
        # Manually build the data list to ensure all fields are properly serialized
        data = []
        for record in records:
            data.append({
                'id': record.id,
                'title': record.title,
                'content': record.content,
                'created_at': record.created_at.isoformat(),
                'updated_at': record.updated_at.isoformat(),
                'expires_at': record.expires_at.isoformat()
            })
        
        # Close the database connection explicitly
        connection.close()
        
        # Return as JSON with proper headers
        response = JsonResponse(data, safe=False)
        response['Access-Control-Allow-Origin'] = '*'  # For development only
        return response
        
    except Exception as e:
        import traceback
        print(f"Error in papan_klip_list_api: {str(e)}")
        print(traceback.format_exc())
        # Return empty array on error to prevent Tabulator errors
        return JsonResponse([], safe=False)

# Class-based Views
class PapanKlipListView(LoginRequiredMixin, ListView):
    model = PapanKlip
    template_name = 'papan_klip/papan_klip_list.html'
    context_object_name = 'papan_klip_records'

class PapanKlipCreateView(LoginRequiredMixin, CreateView):
    model = PapanKlip
    form_class = PapanKlipForm
    template_name = 'papan_klip/papan_klip_form.html'
    success_url = reverse_lazy('papan_klip:papan_klip_list')

class PapanKlipUpdateView(LoginRequiredMixin, UpdateView):
    model = PapanKlip
    form_class = PapanKlipForm
    template_name = 'papan_klip/papan_klip_form.html'
    success_url = reverse_lazy('papan_klip:papan_klip_list')

class PapanKlipDeleteView(LoginRequiredMixin, DeleteView):
    model = PapanKlip
    template_name = 'papan_klip/papan_klip_confirm_delete.html'
    success_url = reverse_lazy('papan_klip:papan_klip_list')
