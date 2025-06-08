from django.urls import path
from . import views

app_name = 'papan_klip'

urlpatterns = [
    path('', views.PapanKlipListView.as_view(), name='papan_klip_list'),
    path('api/', views.papan_klip_list_api, name='papan_klip_list_api'),
    path('create/', views.PapanKlipCreateView.as_view(), name='papan_klip_create'),
    path('<int:pk>/update/', views.PapanKlipUpdateView.as_view(), name='papan_klip_update'),
    path('<int:pk>/delete/', views.PapanKlipDeleteView.as_view(), name='papan_klip_delete'),
]
