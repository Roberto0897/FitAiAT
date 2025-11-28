"""
Configurações de Produção
"""
from .base import *
import dj_database_url
import os
import json

# =============================================================================
# 🔒 SEGURANÇA
# =============================================================================
DEBUG = False
ALLOWED_HOSTS = ['.onrender.com', 'fitaiat.onrender.com']
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# =============================================================================
# 🗄️ BANCO DE DADOS - CORRIGIDO
# =============================================================================
DATABASE_URL = os.environ.get('DATABASE_URL')

print("=" * 60)
print(f"🔍 DATABASE_URL: {DATABASE_URL[:50] if DATABASE_URL else 'NÃO ENCONTRADA'}...")
print("=" * 60)

# Usar parse() diretamente em vez de config()
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
    print(f"✅ HOST configurado: {DATABASES['default'].get('HOST')}")
    print(f"✅ NAME configurado: {DATABASES['default'].get('NAME')}")
else:
    raise Exception("❌ DATABASE_URL não encontrada!")

# =============================================================================
# 🌐 CORS
# =============================================================================
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# 📁 ARQUIVOS ESTÁTICOS
# =============================================================================
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = []  # Remove a pasta static que não existe

if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# =============================================================================
# 🔐 SEGURANÇA HTTPS
# =============================================================================
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# =============================================================================
# 🔥 FIREBASE & GEMINI
# =============================================================================
FIREBASE_CREDENTIALS_JSON = os.environ.get('FIREBASE_CREDENTIALS_JSON')
if FIREBASE_CREDENTIALS_JSON:
    try:
        FIREBASE_CONFIG = json.loads(FIREBASE_CREDENTIALS_JSON)
    except:
        FIREBASE_CONFIG = None
else:
    FIREBASE_CONFIG = None

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
AI_FEATURES_ENABLED = bool(GEMINI_API_KEY)

print("✅ production.py carregado!")