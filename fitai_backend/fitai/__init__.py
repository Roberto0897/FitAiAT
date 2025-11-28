
import os

# 🔥 Define qual settings usar ANTES de qualquer import do Django
if os.environ.get('RENDER') or os.environ.get('DJANGO_SETTINGS_MODULE') == 'fitai.settings.production':
    print("🚀 RENDER/PRODUCTION - Usando production.py")
else:
    print("🏠 LOCAL - Usando development.py")