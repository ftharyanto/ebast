from django.views import View
from django.http import HttpResponse
from django.urls import path
from .views import HomeView, OperatorCreateView, OperatorUpdateView, OperatorListView, OperatorDeleteDirectView, OperatorBulkCreateView
from . import views

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='core'),
    path('operator/', OperatorListView.as_view(), name='operator_list'),
    path('operator/create/', OperatorCreateView.as_view(), name='operator_create'),
    path('operator/update/<int:pk>/', OperatorUpdateView.as_view(), name='operator_update'),
    path('operator/delete-direct/<int:pk>/', OperatorDeleteDirectView.as_view(), name='operator_delete_direct'),
    path('operator/bulk-create/', OperatorBulkCreateView.as_view(), name='operator_bulk_create'),
]