from django.views import View
from django.http import HttpResponse
from django.urls import path
from .views import QcRecordListView, QcRecordCreateView, QcRecordUpdateView, QcRecordDeleteView, fetch_data
from . import views

app_name = 'qc'

urlpatterns = [
    path('', QcRecordListView.as_view(), name='qcrecord_list'),
    path('create/', QcRecordCreateView.as_view(), name='qcrecord_create'),
    path('update/<int:pk>/', QcRecordUpdateView.as_view(), name='qcrecord_update'),
    path('delete/<int:pk>/', QcRecordDeleteView.as_view(), name='qcrecord_delete'),
    path('fetch-data/<str:start_datetime>/<str:end_datetime>/', fetch_data, name='fetch_data'),
    path('api/get_nip/<int:operator_id>/', views.get_nip, name='get_nip'),
]