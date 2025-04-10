from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Estudiante, Curso, Grado, Nota
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

# Create your views here.

def inicio(request):
    try:
        total_estudiantes = Estudiante.objects.count()
        estudiantes_activos = Estudiante.objects.filter(situacion='Activo').count()
        estudiantes_inactivos = Estudiante.objects.filter(situacion='Inactivo').count()
        total_grados = Grado.objects.count()
        total_cursos = Curso.objects.count()
        grados = Grado.objects.all().order_by('nombre')[:5]  # Últimos 5 grados
        cursos = Curso.objects.all().order_by('-id')[:5]  # Últimos 5 cursos
    except Exception as e:
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

class GradoListView(ListView):
    model = Grado
    template_name = 'gestion_estudiantes/grado_list.html'
    context_object_name = 'grados'
    ordering = ['nombre']

class GradoCreateView(CreateView):
    model = Grado
    template_name = 'gestion_estudiantes/grado_form.html'
    fields = ['nombre', 'descripcion', 'duracion']
    success_url = reverse_lazy('grado-list')

    def form_valid(self, form):
        messages.success(self.request, 'Grado creado exitosamente.')
        return super().form_valid(form)

class GradoUpdateView(UpdateView):
    model = Grado
    template_name = 'gestion_estudiantes/grado_form.html'
    fields = ['nombre', 'descripcion', 'duracion']
    success_url = reverse_lazy('grado-list')

    def form_valid(self, form):
        messages.success(self.request, 'Grado actualizado exitosamente.')
        return super().form_valid(form)

class GradoDeleteView(DeleteView):
    model = Grado
    template_name = 'gestion_estudiantes/grado_confirm_delete.html'
    success_url = reverse_lazy('grado-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Grado eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class GradoDetailView(DetailView):
    model = Grado
    template_name = 'gestion_estudiantes/grado_detail.html'
    context_object_name = 'grado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiantes'] = self.object.estudiantes.all()
        context['cursos'] = self.object.cursos.all()
        return context

class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'gestion_estudiantes/estudiante_list.html'
    context_object_name = 'estudiantes'

    def get_queryset(self):
        queryset = Estudiante.objects.all()
        grado_id = self.request.GET.get('grado')
        if grado_id:
            queryset = queryset.filter(grado_id=grado_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grados'] = Grado.objects.all()
        return context

class EstudianteCreateView(CreateView):
    model = Estudiante
    template_name = 'gestion_estudiantes/estudiante_form.html'
    fields = ['nombre', 'fecha_nacimiento', 'sexo', 'situacion', 'grado']
    success_url = reverse_lazy('estudiante-list')

    def form_valid(self, form):
        messages.success(self.request, 'Estudiante creado exitosamente.')
        return super().form_valid(form)

class EstudianteUpdateView(UpdateView):
    model = Estudiante
    template_name = 'gestion_estudiantes/estudiante_form.html'
    fields = ['nombre', 'fecha_nacimiento', 'sexo', 'situacion', 'grado']
    success_url = reverse_lazy('estudiante-list')

    def form_valid(self, form):
        messages.success(self.request, 'Estudiante actualizado exitosamente.')
        return super().form_valid(form)

class EstudianteDeleteView(DeleteView):
    model = Estudiante
    template_name = 'gestion_estudiantes/estudiante_confirm_delete.html'
    success_url = reverse_lazy('estudiante-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Estudiante eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class CursoCreateView(CreateView):
    model = Curso
    template_name = 'gestion_estudiantes/curso_form.html'
    fields = ['nombre', 'codigo', 'creditos', 'semestre']

    def form_valid(self, form):
        grado = get_object_or_404(Grado, pk=self.kwargs['grado_pk'])
        form.instance.grado = grado
        messages.success(self.request, 'Curso creado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('grado-detail', kwargs={'pk': self.kwargs['grado_pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grado'] = get_object_or_404(Grado, pk=self.kwargs['grado_pk'])
        return context

class CursoUpdateView(UpdateView):
    model = Curso
    template_name = 'gestion_estudiantes/curso_form.html'
    fields = ['nombre', 'codigo', 'creditos', 'semestre']

    def get_success_url(self):
        return reverse_lazy('grado-detail', kwargs={'pk': self.object.grado.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grado'] = self.object.grado
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Curso actualizado exitosamente.')
        return super().form_valid(form)

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'gestion_estudiantes/curso_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('grado-detail', kwargs={'pk': self.object.grado.id})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Curso eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = 'gestion_estudiantes/estudiante_detail.html'
    context_object_name = 'estudiante'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notas'] = self.object.notas.all()
        return context

class AsignarCursoForm(forms.Form):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, grado, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['curso'].queryset = Curso.objects.filter(grado=grado)

class AsignarCursoView(FormView):
    template_name = 'gestion_estudiantes/asignar_curso.html'
    form_class = AsignarCursoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        estudiante = get_object_or_404(Estudiante, pk=self.kwargs['estudiante_pk'])
        kwargs['grado'] = estudiante.grado
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiante'] = get_object_or_404(Estudiante, pk=self.kwargs['estudiante_pk'])
        return context

    def form_valid(self, form):
        estudiante = get_object_or_404(Estudiante, pk=self.kwargs['estudiante_pk'])
        curso = form.cleaned_data['curso']
        estudiante.cursos.add(curso)
        messages.success(self.request, f'Curso {curso.nombre} asignado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('estudiante-detail', kwargs={'pk': self.kwargs['estudiante_pk']})

class NotaForm(forms.ModelForm):
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
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiante'] = self.estudiante
        context['curso'] = self.curso
        return context

    def form_valid(self, form):
        form.instance.estudiante = self.estudiante
        form.instance.curso = self.curso
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
