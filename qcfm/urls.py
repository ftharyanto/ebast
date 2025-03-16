from django.urls import path
from .views import QcFmRecordListView, QcFmRecordCreateView, QcFmRecordUpdateView, fetch_data, export_to_excel, QcFmRecordDeleteDirectView
from . import views

app_name = 'qcfm'

urlpatterns = [
    path('', QcFmRecordListView.as_view(), name='qcfmrecord_list'),
    path('create/', QcFmRecordCreateView.as_view(), name='qcfmrecord_create'),
    path('update/<int:pk>/', QcFmRecordUpdateView.as_view(), name='qcfmrecord_update'),
    path('fetch-data/<str:start_datetime>/<str:end_datetime>/', fetch_data, name='fetch_data'),
    path('api/get_nip/<int:operator_id>/', views.get_nip, name='get_nip'),
    path('export-to-excel/<int:record_id>/', export_to_excel, name='export_to_excel'),
    path('export-to-pdf/<int:record_id>/', views.export_to_pdf, name='export_to_pdf'),
    path('delete-direct/<int:pk>/', QcFmRecordDeleteDirectView.as_view(), name='qcfmrecord_delete_direct'),
]