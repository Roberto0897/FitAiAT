#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    
    # 🔥 USA 'RENDER' OU 'DATABASE_URL' - EXISTEM NO BUILD E RUNTIME
    if os.environ.get('RENDER') or os.environ.get('DATABASE_URL'):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'fitai.settings.production'
        print("\n" + "=" * 80)
        print("🚀 RENDER DETECTADO - FORÇANDO production.py")
        print(f"📍 RENDER: {os.environ.get('RENDER')}")
        print(f"📍 DATABASE_URL: {'SIM' if os.environ.get('DATABASE_URL') else 'NÃO'}")
        print("=" * 80 + "\n")
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitai.settings.development')
        print("🏠 LOCAL - Usando development.py")
    
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