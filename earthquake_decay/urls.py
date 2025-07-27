from django.urls import path
from . import views

app_name = 'earthquake_decay'

urlpatterns = [
    path('', views.index, name='index'),
]
