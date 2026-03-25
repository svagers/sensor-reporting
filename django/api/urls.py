from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('api/measurements', views.MeasurementsView.as_view(), name='measurements'),
    path('api/structure', views.StructureView.as_view(), name='structure'),
]
