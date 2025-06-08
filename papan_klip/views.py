import os
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
                'file_url': record.file.url if record.file else None,
                'file_name': record.file.name.split('/')[-1] if record.file else None,
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
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class PapanKlipUpdateView(LoginRequiredMixin, UpdateView):
    model = PapanKlip
    form_class = PapanKlipForm
    template_name = 'papan_klip/papan_klip_form.html'
    success_url = reverse_lazy('papan_klip:papan_klip_list')
    
    def form_valid(self, form):
        # Handle file deletion if the clear checkbox is checked
        if 'file-clear' in self.request.POST:
            if self.object.file:
                self.object.file.delete(save=False)
        return super().form_valid(form)

class PapanKlipDeleteView(LoginRequiredMixin, DeleteView):
    model = PapanKlip
    template_name = 'papan_klip/papan_klip_confirm_delete.html'
    success_url = reverse_lazy('papan_klip:papan_klip_list')
    
    def delete(self, request, *args, **kwargs):
        # Get the object first
        self.object = self.get_object()
        
        # Store the file path before deletion
        file_path = self.object.file.path if self.object.file else None
        
        # Delete the object (this will trigger the model's delete() method)
        response = super().delete(request, *args, **kwargs)
        
        # Double-check if file still exists and delete it
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        
        return response
