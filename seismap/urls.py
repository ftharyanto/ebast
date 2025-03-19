from django.urls import path
from .views import SeismapView

app_name = 'seismap'

urlpatterns = [
    path('', SeismapView.as_view(), name='seismap_view'),]