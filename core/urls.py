from django.views import View
from django.http import HttpResponse
from django.urls import path
from .views import (
    HomeView, OperatorCreateView, OperatorUpdateView, OperatorListView, 
    OperatorDeleteDirectView, OperatorBulkCreateView, KelompokCreateView, 
    KelompokUpdateView, KelompokListView, KelompokDeleteDirectView
)
from . import views

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='core'),
    path('operator/', OperatorListView.as_view(), name='operator_list'),
    path('operator/create/', OperatorCreateView.as_view(), name='operator_create'),
    path('operator/update/<int:pk>/', OperatorUpdateView.as_view(), name='operator_update'),
    path('operator/delete-direct/<int:pk>/', OperatorDeleteDirectView.as_view(), name='operator_delete_direct'),
    path('operator/bulk-create/', OperatorBulkCreateView.as_view(), name='operator_bulk_create'),
    path('kelompok/', KelompokListView.as_view(), name='kelompok_list'),
    path('kelompok/create/', KelompokCreateView.as_view(), name='kelompok_create'),
    path('kelompok/update/<int:pk>/', KelompokUpdateView.as_view(), name='kelompok_update'),
    path('kelompok/delete-direct/<int:pk>/', KelompokDeleteDirectView.as_view(), name='kelompok_delete_direct'),
    path('api/get_operator_list/', views.get_operator_list, name='get_operator_list'),
]