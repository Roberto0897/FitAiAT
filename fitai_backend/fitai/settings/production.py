"""
Configurações para PRODUÇÃO (Render.com)
Usando PostgreSQL do Neon.tech - dados persistentes!
"""

# ==============================================================================
# 🔍 DIAGNÓSTICO - REMOVE DEPOIS QUE FUNCIONAR
# ==============================================================================
import sys
print("=" * 80)
print("🔍 DIAGNÓSTICO DO PRODUCTION.PY")
print(f"📍 Arquivo sendo executado: {__file__}")
print(f"🐍 Python: {sys.version}")
print(f"📂 Path: {sys.path[:3]}")
print("=" * 80)

from .base import *
import os
import json

# ==============================================================================
# 🔒 SEGURANÇA
# ==============================================================================
DEBUG = False

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, '.onrender.com']
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# ==============================================================================
# 🗄️ BANCO DE DADOS - NEON POSTGRESQL (CONFIGURAÇÃO DIRETA)
# ==============================================================================

# ✅ CONFIGURAÇÃO DIRETA DO NEON (SEM VARIÁVEIS DE AMBIENTE)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_GShkFM9ZErs3',
        'HOST': 'ep-damp-forest-acrdjkuq-pooler.sa-east-1.aws.neon.tech',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# 🔍 DIAGNÓSTICO DA CONFIGURAÇÃO
print("\n" + "=" * 80)
print("🗄️  CONFIGURAÇÃO DO BANCO DE DADOS:")
print(f"   ENGINE: {DATABASES['default']['ENGINE']}")
print(f"   NAME: {DATABASES['default']['NAME']}")
print(f"   USER: {DATABASES['default']['USER']}")
print(f"   HOST: {DATABASES['default']['HOST']}")
print(f"   PORT: {DATABASES['default']['PORT']}")
print("=" * 80 + "\n")

# ==============================================================================
# 🌐 CORS
# ==============================================================================
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ==============================================================================
# 📁 ARQUIVOS ESTÁTICOS (WhiteNoise)
# ==============================================================================
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# WhiteNoise para servir arquivos estáticos
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# ==============================================================================
# 🔐 SEGURANÇA HTTPS
# ==============================================================================
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ==============================================================================
# 🔥 FIREBASE
# ==============================================================================
FIREBASE_CREDENTIALS_JSON = os.environ.get('FIREBASE_CREDENTIALS_JSON')

if FIREBASE_CREDENTIALS_JSON:
    try:
        FIREBASE_CONFIG = json.loads(FIREBASE_CREDENTIALS_JSON)
        print("✅ Firebase configurado via variável de ambiente")
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao parsear FIREBASE_CREDENTIALS_JSON: {e}")
        FIREBASE_CONFIG = None
else:
    FIREBASE_CONFIG = None
    print("⚠️  FIREBASE_CREDENTIALS_JSON não encontrada")

# ==============================================================================
# 🤖 GEMINI AI
# ==============================================================================
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
AI_FEATURES_ENABLED = bool(GEMINI_API_KEY)

if AI_FEATURES_ENABLED:
    print("✅ Gemini AI habilitado")
else:
    print("⚠️  GEMINI_API_KEY não encontrada - AI desabilitado")

# ==============================================================================
# 🎯 INFO FINAL
# ==============================================================================
if RENDER_EXTERNAL_HOSTNAME:
    print("\n" + "=" * 80)
    print("🚀 FITAI - PRODUÇÃO (RENDER)")
    print(f"📍 URL: https://{RENDER_EXTERNAL_HOSTNAME}")
    print(f"🗄️  Banco: PostgreSQL (Neon)")
    print(f"🔥 Firebase: {'✅ Configurado' if FIREBASE_CONFIG else '❌ Não configurado'}")
    print(f"🤖 Gemini: {'✅ Habilitado' if AI_FEATURES_ENABLED else '❌ Desabilitado'}")
    print(f"🔒 Debug: {DEBUG}")
    print("=" * 80 + "\n")