from django.db import migrations

def update_sexo_values(apps, schema_editor):
    Estudiante = apps.get_model('gestion_estudiantes', 'Estudiante')
    # Actualizar valores existentes
    Estudiante.objects.filter(sexo='Masculino').update(sexo='M')
    Estudiante.objects.filter(sexo='Femenino').update(sexo='F')

def revert_sexo_values(apps, schema_editor):
    Estudiante = apps.get_model('gestion_estudiantes', 'Estudiante')
    # Revertir cambios
    Estudiante.objects.filter(sexo='M').update(sexo='Masculino')
    Estudiante.objects.filter(sexo='F').update(sexo='Femenino')

class Migration(migrations.Migration):

    dependencies = [
        ('gestion_estudiantes', '0007_remove_nota_unique_nota_estudiante_curso_and_more'),
    ]

    operations = [
        migrations.RunPython(update_sexo_values, revert_sexo_values),
    ] 