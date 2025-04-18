from django.urls import path
from .views import SeismapView
from . import views

app_name = 'seismap'

urlpatterns = [
    path('', SeismapView.as_view(), name='seismap_view'),
    path('fetch_cmt/', views.fetch_cmt_data, name='fetch_cmt_data'),
]