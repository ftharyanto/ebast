from django.views.generic import TemplateView
from django.shortcuts import redirect, render

class TextFormatterView(TemplateView):
    template_name = 'text_formatter/text_formatter.html'
    context_object_name = 'text_formatter_view'

class TutorialView(TemplateView):
    template_name = 'text_formatter/text_formatter_tutorial.html'
