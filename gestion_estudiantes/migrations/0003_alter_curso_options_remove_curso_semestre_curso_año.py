# Generated by Django 5.1.7 on 2025-04-10 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_estudiantes', '0002_grado_remove_curso_carrera_remove_estudiante_carrera_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curso',
            options={'ordering': ['grado', 'año', 'nombre'], 'verbose_name': 'Curso', 'verbose_name_plural': 'Cursos'},
        ),
        migrations.RemoveField(
            model_name='curso',
            name='semestre',
        ),
        migrations.AddField(
            model_name='curso',
            name='año',
            field=models.PositiveIntegerField(default=1, help_text='Año en el que se dicta el curso'),
            preserve_default=False,
        ),
    ]
