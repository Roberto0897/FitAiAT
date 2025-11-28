"""
Configurações para PRODUÇÃO (Render.com)
Usando PostgreSQL do próprio Render - AUTOMÁTICO!
"""

from .base import *
import os
import json
import dj_database_url

print("\n" + "=" * 80)
print("🚨 PRODUCTION.PY SENDO EXECUTADO AGORA!")
print(f"📍 Arquivo: {__file__}")
print(f"🔑 DATABASE_URL: {os.environ.get('DATABASE_URL', 'NÃO ENCONTRADA')[:50]}...")
print(f"🌍 RENDER: {os.environ.get('RENDER', 'NÃO ENCONTRADA')}")
print("=" * 80 + "\n")

# =============================================================================
#  SEGURANÇA
# =============================================================================
DEBUG = False

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, '.onrender.com']
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# =============================================================================
#  BANCO DE DADOS - RENDER POSTGRESQL (AUTOMÁTICO!)
# =============================================================================

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Fix: Render usa 'postgres://' mas Django precisa 'postgresql://'
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
    print("✅ Usando Render PostgreSQL")
    print(f"   Host: {DATABASES['default']['HOST']}")
else:
    print("⚠️  DATABASE_URL não encontrada!")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =============================================================================
#  CORS
# =============================================================================
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# =============================================================================
#  ARQUIVOS ESTÁTICOS
# =============================================================================
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# =============================================================================
#  SEGURANÇA HTTPS
# =============================================================================
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# =============================================================================
#  FIREBASE
# =============================================================================
FIREBASE_CREDENTIALS_JSON = os.environ.get('FIREBASE_CREDENTIALS_JSON')

if FIREBASE_CREDENTIALS_JSON:
    try:
        FIREBASE_CONFIG = json.loads(FIREBASE_CREDENTIALS_JSON)
        print("✅ Firebase configurado")
    except json.JSONDecodeError:
        FIREBASE_CONFIG = None
else:
    FIREBASE_CONFIG = None

# =============================================================================
#  GEMINI AI
# =============================================================================
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
AI_FEATURES_ENABLED = bool(GEMINI_API_KEY)

# =============================================================================
#  INFO FINAL
# =============================================================================
if RENDER_EXTERNAL_HOSTNAME:
    print("\n" + "=" * 80)
    print("🚀 FITAI - PRODUÇÃO")
    print(f"📍 {RENDER_EXTERNAL_HOSTNAME}")
    print(f"🗄️  Banco: {'Render PostgreSQL ✅' if DATABASE_URL else 'SQLite ⚠️'}")
    print(f"🔥 Firebase: {'✅' if FIREBASE_CONFIG else '❌'}")
    print(f"🤖 Gemini: {'✅' if AI_FEATURES_ENABLED else '❌'}")
    print("=" * 80 + "\n")