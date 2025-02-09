from django.views import View
from django.http import HttpResponse
from django.urls import path
from . import views

app_name = 'bast'

urlpatterns = [
    path('', views.BastRecordListView.as_view(), name='bastrecord_list'),
    path('create/', views.BastRecordCreateView.as_view(), name='bastrecord_create'),
    path('update/<int:pk>/', views.BastRecordUpdateView.as_view(), name='bastrecord_update'),
    path('fetch-data/<str:start_datetime>/<str:end_datetime>/', views.fetch_data, name='fetch_data'),
    path('api/get_nip/<int:operator_id>/', views.get_nip, name='get_nip'),
    path('export-to-excel/<int:record_id>/', views.export_to_excel, name='export_to_excel'),
    path('export-to-pdf/<int:record_id>/', views.export_to_pdf, name='export_to_pdf'),
    path('delete-direct/<int:pk>/', views.BastRecordDeleteDirectView.as_view(), name='bastrecord_delete_direct'),
]