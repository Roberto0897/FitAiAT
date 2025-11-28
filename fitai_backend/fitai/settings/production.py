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

print("\n" + "🔍" * 40)
print("🔍 DIAGNÓSTICO DETALHADO DO BANCO:")
print(f"   DATABASE_URL existe? {bool(DATABASE_URL)}")
if DATABASE_URL:
    print(f"   DATABASE_URL (primeiros 80 chars): {DATABASE_URL[:80]}...")
    print(f"   Começa com postgres://? {DATABASE_URL.startswith('postgres://')}")
print("🔍" * 40 + "\n")

if DATABASE_URL:
    # Fix: Render usa 'postgres://' mas Django precisa 'postgresql://'
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        print("✅ URL convertida de postgres:// para postgresql://")
    
    try:
        parsed_db = dj_database_url.parse(DATABASE_URL)
        DATABASES = {
            'default': parsed_db
        }
        print("\n✅ BANCO DE DADOS CONFIGURADO COM SUCESSO!")
        print(f"   Engine: {DATABASES['default'].get('ENGINE', 'N/A')}")
        print(f"   Host: {DATABASES['default'].get('HOST', 'N/A')}")
        print(f"   Port: {DATABASES['default'].get('PORT', 'N/A')}")
        print(f"   Database: {DATABASES['default'].get('NAME', 'N/A')}")
        print(f"   User: {DATABASES['default'].get('USER', 'N/A')}")
        print()
    except Exception as e:
        print(f"\n❌ ERRO AO PARSEAR DATABASE_URL: {e}")
        print("Usando SQLite como fallback")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    print("\n⚠️  DATABASE_URL NÃO ENCONTRADA!")
    print("   Variáveis de ambiente disponíveis:")
    for key in sorted(os.environ.keys()):
        if 'DATABASE' in key or 'RENDER' in key or 'DJANGO' in key:
            print(f"   - {key}: {str(os.environ[key])[:50]}...")
    print()
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