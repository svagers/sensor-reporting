from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('api/sensors', views.SensorsView.as_view(), name='sensors'),
    path('api/structure', views.StructureView.as_view(), name='structure'),
]
