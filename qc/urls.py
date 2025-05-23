from django.views import View
from django.http import HttpResponse
from django.urls import path
from .views import QcRecordListView, QcRecordCreateView, QcRecordUpdateView, fetch_data, export_to_excel, QcRecordDeleteDirectView, ErrorStationListView, ErrorStationCreateView, ErrorStationUpdateView, ErrorStationDeleteView
from . import views

app_name = 'qc'

urlpatterns = [
    path('', QcRecordListView.as_view(), name='qcrecord_list'),
    path('all_records/', views.QcAllRecordsView.as_view(), name='qc_all_records'),
    path('create/', QcRecordCreateView.as_view(), name='qcrecord_create'),
    path('update/<int:pk>/', QcRecordUpdateView.as_view(), name='qcrecord_update'),
    path('fetch-data/<str:start_datetime>/<str:end_datetime>/', fetch_data, name='fetch_data'),
    path('api/qcrecord-list/<int:counts>/', views.qcrecord_list_api, name='qcrecord_list_api'),
    path('api/get_nip/<int:operator_id>/', views.get_nip, name='get_nip'),
    path('api/export-to-excel/<int:record_id>/', views.export_to_excel, name='export_to_excel'),
    path('api/export-to-pdf/<int:record_id>/', views.export_to_pdf, name='export_to_pdf'),
    path('delete-direct/<int:pk>/', QcRecordDeleteDirectView.as_view(), name='qcrecord_delete_direct'),
    path('save-nip/', views.save_nip, name='save_nip'),
    path('errorstations/', ErrorStationListView.as_view(), name='errorstation_list'),
    path('errorstations/add/', ErrorStationCreateView.as_view(), name='errorstation_add'),
    path('errorstations/<int:pk>/edit/', ErrorStationUpdateView.as_view(), name='errorstation_edit'),
    path('errorstations/<int:pk>/delete/', ErrorStationDeleteView.as_view(), name='errorstation_delete'),
    path('api/export-csv/', views.export_qc_to_csv, name='export_qc_csv'),
]