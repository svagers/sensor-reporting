from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/info', views.Info.as_view(), name='api-info'),
    path('api/sensors', views.SensorsView.as_view(), name='sensors'),
    path('api/structure', views.StructureView.as_view(), name='structure'),
    path('', views.welcome_page, name='welcome'),
]
