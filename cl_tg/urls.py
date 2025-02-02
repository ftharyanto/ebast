from django.views import View
from django.http import HttpResponse
from django.urls import path
from .views import CtgListView, StationListView, StationCreateView, StationUpdateView, StationDeleteView, StationBulkCreateView, CtgCreateView, CtgUpdateView, CtgDeleteView, ctg_export_excel, ctg_export_pdf
from . import views

app_name = 'cl_tg'

urlpatterns = [
    path('', CtgListView.as_view(), name='ctg_list'),
    path('station_list/', StationListView.as_view(), name='station_list'),
    path('station/create/', StationCreateView.as_view(), name='sl_create'),
    path('station/update/<int:pk>/', StationUpdateView.as_view(), name='sl_update'),
    path('station/delete/<int:pk>/', StationDeleteView.as_view(), name='sl_delete'),
    path('station/bulk_create/', StationBulkCreateView.as_view(), name='sl_bulk_create'),
    path('ctg/create/', CtgCreateView.as_view(), name='ctg_create'),
    path('ctg/update/<int:pk>/', CtgUpdateView.as_view(), name='ctg_update'),
    path('ctg/delete/<int:pk>/', CtgDeleteView.as_view(), name='ctg_delete'),
    path('cs-export-excel/<int:record_id>/', ctg_export_excel, name='ctg_export_excel'),
    path('cs-export-pdf/<int:record_id>/', ctg_export_pdf, name='ctg_export_pdf'),
]