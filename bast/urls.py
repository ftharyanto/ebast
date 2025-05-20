from django.views import View
from django.http import HttpResponse
from django.urls import path
from . import views

app_name = 'bast'

urlpatterns = [
    path('', views.BastRecordListView.as_view(), name='bastrecord_list'),
    path('grid/', views.BastRecordGridView.as_view(), name='bastrecord_grid'),
    path('gridjs/', views.BastRecordGridJSView.as_view(), name='bastrecord_gridjs'),
    path('tabulator/', views.BastRecordTabulatorView.as_view(), name='bastrecord_tabulator'),
    path('create/', views.BastRecordCreateView.as_view(), name='bastrecord_create'),
    path('update/<int:pk>/', views.BastRecordUpdateView.as_view(), name='bastrecord_update'),
    path('api/bastrecord-list/', views.bastrecord_list_api, name='bastrecord_list_api'),
    path('fetch-data/<str:start_datetime>/<str:end_datetime>/', views.fetch_data, name='fetch_data'),
    path('api/get_nip/<int:operator_id>/', views.get_nip, name='get_nip'),
    path('api/get_member_data/<int:kelompok>/', views.get_member_data, name='get_member_data'),
    path('api/get_cs_data/<str:cs_id>/', views.get_cs_data, name='get_cs_data'),
    path('export-to-excel/<int:record_id>/', views.export_to_excel, name='export_to_excel'),
    path('export-to-pdf/<int:record_id>/', views.export_to_pdf, name='export_to_pdf'),
    path('delete-direct/<int:pk>/', views.BastRecordDeleteDirectView.as_view(), name='bastrecord_delete_direct'),
    path('api/get_previous_members/', views.get_previous_members, name='get_previous_members'),
    path('api/get_previous_poco_exp/', views.get_previous_poco_exp, name='get_previous_poco_exp'),
    path('api/get_previous_samsung_exp/', views.get_previous_samsung_exp, name='get_previous_samsung_exp'),
    path('api/get_previous_pulsa_poco/', views.get_previous_pulsa_poco, name='get_previous_pulsa_poco'),
]