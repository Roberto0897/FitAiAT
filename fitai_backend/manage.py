#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    
    # 🔍 DETECTA SE ESTÁ NO RENDER
    # Render injeta a variável RENDER quando faz deploy
    is_render = os.environ.get('RENDER') is not None
    
    if is_render:
        # 🚀 NO RENDER: Usa production
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitai.settings.production')
        print("🔥 Render detectado - Usando fitai.settings.production")
    else:
        # 🏠 LOCAL: Usa development
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitai.settings.development')
        print("🏠 Ambiente local - Usando fitai.settings.development")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()