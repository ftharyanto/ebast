from django.views import View
from django.http import HttpResponse
from django.urls import path
from .views import CsListView, StationListView, StationCreateView, StationUpdateView, StationDeleteView, StationBulkCreateView
from . import views

app_name = 'cl_seiscomp'

urlpatterns = [
    path('', CsListView.as_view(), name='cs_list'),
    path('station_list/', StationListView.as_view(), name='station_list'),
    path('station/create/', StationCreateView.as_view(), name='sl_create'),
    path('station/update/<int:pk>/', StationUpdateView.as_view(), name='sl_update'),
    path('station/delete/<int:pk>/', StationDeleteView.as_view(), name='sl_delete'),
    path('station/bulk_create/', StationBulkCreateView.as_view(), name='sl_bulk_create'),
]