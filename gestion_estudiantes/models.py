from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Grado(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    duracion = models.PositiveIntegerField(help_text="Duración en años")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
        ordering = ['nombre']

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=10, unique=True)
    creditos = models.PositiveIntegerField()
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='cursos', null=True, blank=True)
    semestre = models.PositiveIntegerField(help_text="Semestre en el que se dicta el curso")

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['grado', 'semestre', 'nombre']

class Estudiante(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    ]
    
    SITUACION_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo')
    ]
    
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    situacion = models.CharField(max_length=10, choices=SITUACION_CHOICES, default='Activo')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='estudiantes', null=True, blank=True)
    cursos = models.ManyToManyField(Curso, related_name='estudiantes', blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['nombre']

class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='notas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='notas')
    nota = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    fecha_registro = models.DateTimeField(auto_now=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.curso.nombre}: {self.nota}"

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = ['estudiante', 'curso']  # Un estudiante solo puede tener una nota por curso
        ordering = ['-fecha_registro']
