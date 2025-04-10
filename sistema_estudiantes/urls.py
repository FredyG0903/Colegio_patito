from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from gestion_estudiantes.views import inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio, name='inicio'),
    path('', RedirectView.as_view(url='inicio/', permanent=False)),
    path('estudiantes/', include('gestion_estudiantes.urls')),
] 