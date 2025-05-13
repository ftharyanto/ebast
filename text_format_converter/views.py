from django.views.generic import TemplateView
from django.shortcuts import redirect, render

class ConverterView(TemplateView):
    template_name = 'text_format_converter/converter.html'
    context_object_name = 'converter_view'

class TutorialView(TemplateView):
    template_name = 'text_format_converter/tutorial.html'
