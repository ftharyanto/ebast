from django.views import View
from django.http import HttpResponse
from django.urls import path
from .views import TextFormatterView, TutorialView
from . import views

app_name = 'text_formatter'

urlpatterns = [
    path('', TextFormatterView.as_view(), name='text_formatter_view'),
    path('tutorial/', TutorialView.as_view(), name='text_formatter_tutorial'),
]