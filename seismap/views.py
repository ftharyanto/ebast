from django.views.generic import TemplateView
from django.shortcuts import redirect

class SeismapView(TemplateView):
    template_name = 'seismap/seismap.html'
    context_object_name = 'seismap_view'
