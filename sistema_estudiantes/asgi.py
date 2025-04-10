"""
ASGI config for sistema_estudiantes project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_estudiantes.settings')

application = get_asgi_application() 