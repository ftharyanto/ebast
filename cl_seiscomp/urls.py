from django.views import View
from django.http import HttpResponse
from django.urls import path
from .views import CsListView, StationListView, StationCreateView, StationUpdateView, StationDeleteView, StationBulkCreateView, CsCreateView, CsUpdateView, CsDeleteView, export_to_excel, export_to_pdf, fetch_gaps_blanks, export_cs_to_csv
from . import views

app_name = 'cl_seiscomp'

urlpatterns = [
    path('', CsListView.as_view(), name='cs_list'),
    path('all_records/', views.CsAllRecordsView.as_view(), name='cs_all_records'),
    path('station_list/', StationListView.as_view(), name='station_list'),
    path('station/create/', StationCreateView.as_view(), name='sl_create'),
    path('station/update/<int:pk>/', StationUpdateView.as_view(), name='sl_update'),
    path('station/delete/<int:pk>/', StationDeleteView.as_view(), name='sl_delete'),
    path('station/bulk_create/', StationBulkCreateView.as_view(), name='sl_bulk_create'),
    path('cs/create/', CsCreateView.as_view(), name='cs_create'),
    path('cs/update/<int:pk>/', CsUpdateView.as_view(), name='cs_update'),
    path('cs/delete/<int:pk>/', CsDeleteView.as_view(), name='cs_delete'),
    path('api/csrecord-list/<int:counts>/', views.csrecord_list_api, name='csrecord_list_api'),
    path('api/export-to-excel/<int:record_id>/', export_to_excel, name='export_to_excel'),
    path('api/export-to-pdf/<int:record_id>/', export_to_pdf, name='export_to_pdf'),
    path('api/export-csv/', export_cs_to_csv, name='export_cs_to_csv'),
    path('cs/fetch_gaps_blanks/', fetch_gaps_blanks, name='fetch_gaps_blanks'),
    path('stats/', views.StatsView.as_view(), name='stats'),
]