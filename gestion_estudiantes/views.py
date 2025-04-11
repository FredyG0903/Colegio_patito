"""
Views para el sistema de gestión escolar del Colegio El Patito.
Este módulo contiene todas las vistas necesarias para gestionar estudiantes, grados, cursos y notas.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Estudiante, Curso, Grado, Nota
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

# Create your views here.

def inicio(request):
    """
    Vista principal del dashboard que muestra estadísticas generales del sistema.
    Incluye conteos de estudiantes, grados y cursos, así como listas resumidas.
    """
    try:
        # Obtener estadísticas generales
        total_estudiantes = Estudiante.objects.count()
        estudiantes_activos = Estudiante.objects.filter(situacion='Activo').count()
        estudiantes_inactivos = Estudiante.objects.filter(situacion='Inactivo').count()
        total_grados = Grado.objects.count()
        total_cursos = Curso.objects.count()
        grados = Grado.objects.all().order_by('nombre')[:5]  # Últimos 5 grados
        cursos = Curso.objects.all().order_by('-id')[:5]  # Últimos 5 cursos
    except Exception as e:
        # Manejo de errores en caso de problemas con la base de datos
        total_estudiantes = 0
        estudiantes_activos = 0
        estudiantes_inactivos = 0
        total_grados = 0
        total_cursos = 0
        grados = []
        cursos = []
        messages.error(request, f'Error al cargar las estadísticas: {str(e)}')

    context = {
        'total_estudiantes': total_estudiantes,
        'estudiantes_activos': estudiantes_activos,
        'estudiantes_inactivos': estudiantes_inactivos,
        'total_grados': total_grados,
        'total_cursos': total_cursos,
        'grados': grados,
        'cursos': cursos,
    }
    return render(request, 'gestion_estudiantes/inicio.html', context)

# Vistas relacionadas con Grados
class GradoListView(ListView):
    """Vista para listar todos los grados académicos."""
    model = Grado
    template_name = 'gestion_estudiantes/grado_list.html'
    context_object_name = 'grados'
    ordering = ['nombre']

class GradoCreateView(CreateView):
    """Vista para crear un nuevo grado académico."""
    model = Grado
    template_name = 'gestion_estudiantes/grado_form.html'
    fields = ['nombre', 'descripcion', 'duracion']
    success_url = reverse_lazy('grado-list')

    def form_valid(self, form):
        """Método ejecutado cuando el formulario es válido."""
        messages.success(self.request, 'Grado creado exitosamente.')
        return super().form_valid(form)

class GradoUpdateView(UpdateView):
    """Vista para actualizar un grado existente."""
    model = Grado
    template_name = 'gestion_estudiantes/grado_form.html'
    fields = ['nombre', 'descripcion', 'duracion']
    success_url = reverse_lazy('grado-list')

    def form_valid(self, form):
        """Método ejecutado cuando el formulario es válido."""
        messages.success(self.request, 'Grado actualizado exitosamente.')
        return super().form_valid(form)

class GradoDeleteView(DeleteView):
    """Vista para eliminar un grado existente."""
    model = Grado
    template_name = 'gestion_estudiantes/grado_confirm_delete.html'
    success_url = reverse_lazy('grado-list')

    def delete(self, request, *args, **kwargs):
        """Método ejecutado cuando se confirma la eliminación."""
        messages.success(request, 'Grado eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class GradoDetailView(DetailView):
    """Vista para ver los detalles de un grado específico."""
    model = Grado
    template_name = 'gestion_estudiantes/grado_detail.html'
    context_object_name = 'grado'

    def get_context_data(self, **kwargs):
        """Agrega estudiantes y cursos relacionados al contexto."""
        context = super().get_context_data(**kwargs)
        context['estudiantes'] = self.object.estudiantes.all()
        context['cursos'] = self.object.cursos.all()
        context['cursos_por_año'] = self.object.cursos.all().order_by('año')
        return context

# Vistas relacionadas con Estudiantes
class EstudianteListView(ListView):
    """Vista para listar todos los estudiantes con opciones de filtrado."""
    model = Estudiante
    template_name = 'gestion_estudiantes/estudiante_list.html'
    context_object_name = 'estudiantes'

    def get_queryset(self):
        """Filtra estudiantes por grado e ID si se especifican en la URL."""
        queryset = Estudiante.objects.all()
        grado_id = self.request.GET.get('grado')
        estudiante_id = self.request.GET.get('id')
        
        if grado_id:
            queryset = queryset.filter(grado_id=grado_id)
        if estudiante_id:
            queryset = queryset.filter(id_estudiante=estudiante_id)
        
        return queryset

    def get_context_data(self, **kwargs):
        """Agrega lista de grados y el ID de estudiante buscado al contexto."""
        context = super().get_context_data(**kwargs)
        context['grados'] = Grado.objects.all()
        context['estudiante_id'] = self.request.GET.get('id', '')
        return context

class EstudianteCreateView(CreateView):
    """Vista para crear un nuevo estudiante."""
    model = Estudiante
    template_name = 'gestion_estudiantes/estudiante_form.html'
    fields = ['id_estudiante', 'nombre', 'fecha_nacimiento', 'sexo', 'situacion', 'grado']
    success_url = reverse_lazy('estudiante-list')

    def form_valid(self, form):
        """Método ejecutado cuando el formulario es válido."""
        messages.success(self.request, 'Estudiante creado exitosamente.')
        return super().form_valid(form)

class EstudianteUpdateView(UpdateView):
    """Vista para actualizar un estudiante existente."""
    model = Estudiante
    template_name = 'gestion_estudiantes/estudiante_form.html'
    fields = ['id_estudiante', 'nombre', 'fecha_nacimiento', 'sexo', 'situacion', 'grado']
    success_url = reverse_lazy('estudiante-list')

    def form_valid(self, form):
        """Método ejecutado cuando el formulario es válido."""
        messages.success(self.request, 'Estudiante actualizado exitosamente.')
        return super().form_valid(form)

class EstudianteDeleteView(DeleteView):
    """Vista para eliminar un estudiante existente."""
    model = Estudiante
    template_name = 'gestion_estudiantes/estudiante_confirm_delete.html'
    success_url = reverse_lazy('estudiante-list')

    def delete(self, request, *args, **kwargs):
        """Método ejecutado cuando se confirma la eliminación."""
        messages.success(request, 'Estudiante eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

# Vistas relacionadas con Cursos
class CursoCreateView(CreateView):
    """Vista para crear un nuevo curso dentro de un grado específico."""
    model = Curso
    template_name = 'gestion_estudiantes/curso_form.html'
    fields = ['nombre', 'codigo', 'creditos', 'año']

    def form_valid(self, form):
        """Asigna el grado al curso y guarda el formulario."""
        grado = get_object_or_404(Grado, pk=self.kwargs['grado_pk'])
        form.instance.grado = grado
        messages.success(self.request, 'Curso creado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        """Redirecciona a los detalles del grado después de crear el curso."""
        return reverse_lazy('grado-detail', kwargs={'pk': self.kwargs['grado_pk']})

    def get_context_data(self, **kwargs):
        """Agrega el grado al contexto del formulario."""
        context = super().get_context_data(**kwargs)
        context['grado'] = get_object_or_404(Grado, pk=self.kwargs['grado_pk'])
        return context

class CursoUpdateView(UpdateView):
    """Vista para actualizar un curso existente."""
    model = Curso
    template_name = 'gestion_estudiantes/curso_form.html'
    fields = ['nombre', 'codigo', 'creditos', 'año']

    def get_success_url(self):
        """Redirecciona a los detalles del grado después de actualizar."""
        return reverse_lazy('grado-detail', kwargs={'pk': self.object.grado.id})

    def get_context_data(self, **kwargs):
        """Agrega el grado al contexto del formulario."""
        context = super().get_context_data(**kwargs)
        context['grado'] = self.object.grado
        return context

    def form_valid(self, form):
        """Método ejecutado cuando el formulario es válido."""
        messages.success(self.request, 'Curso actualizado exitosamente.')
        return super().form_valid(form)

class CursoDeleteView(DeleteView):
    """Vista para eliminar un curso existente."""
    model = Curso
    template_name = 'gestion_estudiantes/curso_confirm_delete.html'

    def get_success_url(self):
        """Redirecciona a los detalles del grado después de eliminar."""
        return reverse_lazy('grado-detail', kwargs={'pk': self.object.grado.id})

    def delete(self, request, *args, **kwargs):
        """Método ejecutado cuando se confirma la eliminación."""
        messages.success(request, 'Curso eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class EstudianteDetailView(DetailView):
    """Vista para ver los detalles de un estudiante específico."""
    model = Estudiante
    template_name = 'gestion_estudiantes/estudiante_detail.html'
    context_object_name = 'estudiante'

    def get_context_data(self, **kwargs):
        """Agrega las notas del estudiante al contexto."""
        context = super().get_context_data(**kwargs)
        context['notas'] = self.object.notas.all()
        return context

# Formularios y vistas para asignación de cursos
class AsignarCursoForm(forms.Form):
    """Formulario para asignar un curso a un estudiante."""
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, grado, *args, **kwargs):
        """Inicializa el formulario filtrando los cursos por grado."""
        super().__init__(*args, **kwargs)
        self.fields['curso'].queryset = Curso.objects.filter(grado=grado)

class AsignarCursoView(FormView):
    """Vista para asignar un curso a un estudiante."""
    template_name = 'gestion_estudiantes/asignar_curso.html'
    form_class = AsignarCursoForm

    def get_form_kwargs(self):
        """Pasa el grado del estudiante al formulario."""
        kwargs = super().get_form_kwargs()
        estudiante = get_object_or_404(Estudiante, pk=self.kwargs['estudiante_pk'])
        kwargs['grado'] = estudiante.grado
        return kwargs

    def get_context_data(self, **kwargs):
        """Agrega el estudiante al contexto."""
        context = super().get_context_data(**kwargs)
        context['estudiante'] = get_object_or_404(Estudiante, pk=self.kwargs['estudiante_pk'])
        return context

    def form_valid(self, form):
        """Asigna el curso seleccionado al estudiante."""
        estudiante = get_object_or_404(Estudiante, pk=self.kwargs['estudiante_pk'])
        curso = form.cleaned_data['curso']
        estudiante.cursos.add(curso)
        messages.success(self.request, f'Curso {curso.nombre} asignado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        """Redirecciona a los detalles del estudiante después de asignar el curso."""
        return reverse_lazy('estudiante-detail', kwargs={'pk': self.kwargs['estudiante_pk']})

# Formularios y vistas para gestión de notas
class NotaForm(forms.ModelForm):
    """Formulario para crear y editar notas."""
    class Meta:
        model = Nota
        fields = ['nota', 'observaciones']
        widgets = {
            'nota': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': 'Ingrese una nota entre 0 y 100'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Observaciones opcionales'
            }),
        }
        help_texts = {
            'nota': 'Ingrese una nota entre 0 y 100',
            'observaciones': 'Observaciones adicionales sobre la nota'
        }

class NotaCreateView(CreateView):
    model = Nota
    form_class = NotaForm
    template_name = 'gestion_estudiantes/nota_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.estudiante = get_object_or_404(Estudiante, pk=kwargs['estudiante_pk'])
        self.curso = get_object_or_404(Curso, pk=kwargs['curso_pk'])
        if not self.estudiante.id_estudiante:
            messages.error(request, 'El estudiante no tiene un ID asignado.')
            return redirect('estudiante-detail', pk=self.estudiante.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiante'] = self.estudiante
        context['curso'] = self.curso
        # Verificar si ya existe una nota para este estudiante y curso
        nota_existente = Nota.objects.filter(
            estudiante_id_form=self.estudiante.id_estudiante,
            curso_codigo=self.curso.codigo
        ).first()
        if nota_existente:
            context['nota_existente'] = nota_existente
            messages.warning(self.request, f'Ya existe una nota de {nota_existente.nota} para este estudiante en este curso.')
        return context

    def form_valid(self, form):
        # Verificar si ya existe una nota para este estudiante y curso
        nota_existente = Nota.objects.filter(
            estudiante_id_form=self.estudiante.id_estudiante,
            curso_codigo=self.curso.codigo
        ).first()
        
        if nota_existente:
            messages.error(self.request, 'Ya existe una nota para este estudiante en este curso.')
            return self.form_invalid(form)
            
        form.instance.estudiante = self.estudiante
        form.instance.curso = self.curso
        form.instance.estudiante_nombre = self.estudiante.nombre
        form.instance.estudiante_id_form = self.estudiante.id_estudiante
        form.instance.curso_nombre = self.curso.nombre
        form.instance.curso_codigo = self.curso.codigo
        
        messages.success(self.request, 'Nota registrada exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('estudiante-detail', kwargs={'pk': self.estudiante.pk})

class NotaUpdateView(UpdateView):
    model = Nota
    form_class = NotaForm
    template_name = 'gestion_estudiantes/nota_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiante'] = self.object.estudiante
        context['curso'] = self.object.curso
        return context

    def get_success_url(self):
        return reverse_lazy('estudiante-detail', kwargs={'pk': self.object.estudiante.pk})

class NotaDeleteView(DeleteView):
    model = Nota
    template_name = 'gestion_estudiantes/nota_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('estudiante-detail', kwargs={'pk': self.object.estudiante.pk})
