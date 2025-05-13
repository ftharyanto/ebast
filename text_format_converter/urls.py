from django.views import View
from django.http import HttpResponse
from django.urls import path
from .views import ConverterView, TutorialView
from . import views

app_name = 'text_format_converter'

urlpatterns = [
    path('', ConverterView.as_view(), name='converter_view'),
    path('tutorial/', TutorialView.as_view(), name='tutorial_view'),
]