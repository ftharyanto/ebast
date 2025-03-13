from django.views import View
from django.http import HttpResponse
from django.urls import path
from .views import FmRecordListView, FmRecordCreateView, FmRecordUpdateView, fetch_data, export_to_excel, FmRecordDeleteDirectView
from . import views

app_name = 'fm'

urlpatterns = [
    path('', FmRecordListView.as_view(), name='fmrecord_list'),
    path('create/', FmRecordCreateView.as_view(), name='fmrecord_create'),
    path('update/<int:pk>/', FmRecordUpdateView.as_view(), name='fmrecord_update'),
    path('fetch-data/<str:start_datetime>/<str:end_datetime>/', fetch_data, name='fetch_data'),
    path('api/get_nip/<int:operator_id>/', views.get_nip, name='get_nip'),
    path('export-to-excel/<int:record_id>/', export_to_excel, name='export_to_excel'),
    path('export-to-pdf/<int:record_id>/', views.export_to_pdf, name='export_to_pdf'),
    path('delete-direct/<int:pk>/', FmRecordDeleteDirectView.as_view(), name='fmrecord_delete_direct'),
]