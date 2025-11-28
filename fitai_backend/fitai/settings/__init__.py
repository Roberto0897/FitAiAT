import os

#  DETECTA O AMBIENTE AUTOMATICAMENTE
# RENDER está disponível no build E runtime (RENDER_EXTERNAL_HOSTNAME só no runtime)
if os.environ.get('RENDER') or os.environ.get('DATABASE_URL'):
    print("🚀 RENDER DETECTADO - Carregando production.py")
    from .production import *
else:
    print("🏠 LOCAL - Carregando development.py")
    from .development import *