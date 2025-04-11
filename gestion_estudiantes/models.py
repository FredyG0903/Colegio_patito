from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Modelo para representar los grados académicos
class Grado(models.Model):
    # Campos básicos del grado
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)  # Opcional, puede estar vacío
    duracion = models.PositiveIntegerField(help_text="Duración en años")
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Se establece automáticamente al crear

    def calcular_promedio_general(self):
        """
        Calcula el promedio general de todos los estudiantes en este grado.
        Retorna 0 si no hay estudiantes, de lo contrario retorna el promedio redondeado a 2 decimales.
        """
        estudiantes = self.estudiantes.all()
        if not estudiantes:
            return 0
        total_promedios = sum(estudiante.calcular_promedio() for estudiante in estudiantes)
        return round(total_promedios / estudiantes.count(), 2)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Grado"
        verbose_name_plural = "Grados"
        ordering = ['nombre']  # Ordena los grados por nombre

# Modelo para representar los cursos académicos
class Curso(models.Model):
    # Campos básicos del curso
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=10, unique=True)  # Código único para cada curso
    creditos = models.PositiveIntegerField()
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='cursos', null=True, blank=True)
    año = models.PositiveIntegerField(help_text="Año en el que se dicta el curso")

    def get_nota_estudiante(self, estudiante):
        """
        Obtiene la nota de un estudiante específico en este curso.
        Retorna None si el estudiante no tiene nota en este curso.
        """
        return self.notas.filter(estudiante=estudiante).first()

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['grado', 'año', 'nombre']  # Ordena por grado, año y nombre

# Modelo para representar a los estudiantes
class Estudiante(models.Model):
    # Campos básicos del estudiante
    id_estudiante = models.CharField(max_length=20, verbose_name="ID del Estudiante", unique=True, default='')
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    
    # Opciones para el campo sexo
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    
    # Opciones para el estado del estudiante
    SITUACION_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    situacion = models.CharField(max_length=10, choices=SITUACION_CHOICES)
    
    # Relaciones con otros modelos
    grado = models.ForeignKey(Grado, on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    cursos = models.ManyToManyField(Curso, related_name='estudiantes', blank=True)

    def get_sexo_display(self):
        """
        Retorna la versión legible del sexo del estudiante.
        """
        return 'Masculino' if self.sexo == 'M' else 'Femenino'

    def calcular_promedio(self):
        """
        Calcula el promedio de todas las notas del estudiante.
        Retorna 0 si no tiene notas, de lo contrario retorna el promedio redondeado a 2 decimales.
        """
        notas = self.notas.all()
        if not notas:
            return 0
        total = sum(float(nota.nota) for nota in notas)
        return round(total / len(notas), 2)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['nombre']

# Modelo para representar las notas de los estudiantes en los cursos
class Nota(models.Model):
    # Relaciones con otros modelos
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='notas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='notas')
    
    # Campos para almacenar información redundante (mejora el rendimiento de consultas)
    estudiante_nombre = models.CharField(max_length=100, default='')
    estudiante_id_form = models.CharField(max_length=20, verbose_name="ID del Estudiante", default='')
    curso_nombre = models.CharField(max_length=200, default='')
    curso_codigo = models.CharField(max_length=10, default='')
    
    # Campo para la nota con validadores
    nota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),  # La nota no puede ser menor que 0
            MaxValueValidator(100)  # La nota no puede ser mayor que 100
        ]
    )
    fecha_registro = models.DateTimeField(auto_now=True)  # Se actualiza automáticamente
    observaciones = models.TextField(blank=True, null=True)  # Opcional

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para actualizar los campos redundantes
        antes de guardar una nueva nota.
        """
        if not self.pk:  # Solo si es una nueva nota
            # Guardar información del estudiante y curso
            self.estudiante_nombre = self.estudiante.nombre
            self.estudiante_id_form = self.estudiante.id_estudiante
            self.curso_nombre = self.curso.nombre
            self.curso_codigo = self.curso.codigo
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.estudiante_nombre} ({self.estudiante_id_form}) - {self.curso_nombre} ({self.curso_codigo}): {self.nota}"

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = ['estudiante_id_form', 'curso_codigo']  # Evita notas duplicadas
        ordering = ['-fecha_registro']  # Ordena por fecha de registro, más recientes primero
