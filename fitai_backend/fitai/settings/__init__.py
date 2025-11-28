import os

# 🔥 DETECTA O AMBIENTE AUTOMATICAMENTE
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    # NO RENDER: Força production
    print("🚀 RENDER DETECTADO - Carregando production.py")
    from .production import *
elif os.environ.get('DJANGO_SETTINGS_MODULE') == 'fitai.settings.production':
    # Se explicitamente pediu production
    print("⚙️  PRODUCTION EXPLÍCITO - Carregando production.py")
    from .production import *
else:
    # LOCAL: Usa development
    print("🏠 LOCAL - Carregando development.py")
    from .development import *