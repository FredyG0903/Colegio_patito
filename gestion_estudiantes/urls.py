from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('estudiantes/', views.EstudianteListView.as_view(), name='estudiante-list'),
    path('estudiantes/nuevo/', views.EstudianteCreateView.as_view(), name='estudiante-create'),
    path('estudiantes/<int:pk>/editar/', views.EstudianteUpdateView.as_view(), name='estudiante-update'),
    path('estudiantes/<int:pk>/eliminar/', views.EstudianteDeleteView.as_view(), name='estudiante-delete'),
    path('estudiantes/<int:pk>/', views.EstudianteDetailView.as_view(), name='estudiante-detail'),
    path('estudiantes/<int:estudiante_pk>/asignar-curso/', views.AsignarCursoView.as_view(), name='asignar-curso'),
    path('estudiantes/<int:estudiante_pk>/cursos/<int:curso_pk>/nota/nueva/', views.NotaCreateView.as_view(), name='nota-create'),
    path('notas/<int:pk>/editar/', views.NotaUpdateView.as_view(), name='nota-update'),
    path('notas/<int:pk>/eliminar/', views.NotaDeleteView.as_view(), name='nota-delete'),
    path('grados/', views.GradoListView.as_view(), name='grado-list'),
    path('grados/nuevo/', views.GradoCreateView.as_view(), name='grado-create'),
    path('grados/<int:pk>/editar/', views.GradoUpdateView.as_view(), name='grado-update'),
    path('grados/<int:pk>/eliminar/', views.GradoDeleteView.as_view(), name='grado-delete'),
    path('grados/<int:pk>/', views.GradoDetailView.as_view(), name='grado-detail'),
    path('grados/<int:grado_pk>/cursos/nuevo/', views.CursoCreateView.as_view(), name='curso-create'),
    path('cursos/<int:pk>/editar/', views.CursoUpdateView.as_view(), name='curso-update'),
    path('cursos/<int:pk>/eliminar/', views.CursoDeleteView.as_view(), name='curso-delete'),
] 