from django import template

register = template.Library()

@register.filter
def get_nota_estudiante(notas, estudiante):
    for nota in notas:
        if nota.estudiante == estudiante:
            return nota
    return None 