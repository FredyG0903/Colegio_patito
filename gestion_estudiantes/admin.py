from django.contrib import admin
from .models import Grado, Curso, Estudiante, Nota

@admin.register(Grado)
class GradoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion', 'fecha_creacion')
    search_fields = ('nombre',)
    list_filter = ('fecha_creacion',)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'grado', 'semestre', 'creditos')
    list_filter = ('grado', 'semestre')
    search_fields = ('nombre', 'codigo')

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grado', 'situacion', 'fecha_registro')
    list_filter = ('grado', 'situacion', 'sexo')
    search_fields = ('nombre',)
    filter_horizontal = ('cursos',)

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'curso', 'nota', 'fecha_registro')
    list_filter = ('curso', 'fecha_registro')
    search_fields = ('estudiante__nombre', 'curso__nombre')
