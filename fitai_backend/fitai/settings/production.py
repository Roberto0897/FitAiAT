"""
Configurações para PRODUÇÃO (Render.com)
Usando PostgreSQL do Neon.tech - dados persistentes!
"""
from .base import *
import os
import json
import dj_database_url

# =============================================================================
# 🔒 SEGURANÇA
# =============================================================================

DEBUG = False

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, '.onrender.com']
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# =============================================================================
# 🗄️ BANCO DE DADOS - NEON POSTGRESQL
# =============================================================================

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Neon PostgreSQL (produção)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
    print("✅ Usando Neon PostgreSQL (dados persistentes)")
else:
    # Fallback SQLite (desenvolvimento)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("⚠️ DATABASE_URL não configurada - usando SQLite local")

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

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# =============================================================================
# 🔥 FIREBASE
# =============================================================================

FIREBASE_CREDENTIALS_JSON = os.environ.get('FIREBASE_CREDENTIALS')

if FIREBASE_CREDENTIALS_JSON:
    try:
        import firebase_admin
        from firebase_admin import credentials
        
        firebase_config = json.loads(FIREBASE_CREDENTIALS_JSON)
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase inicializado")
    except Exception as e:
        print(f"⚠️ Firebase: {e}")
else:
    print("⚠️ FIREBASE_CREDENTIALS não configurada")

# =============================================================================
# 🤖 GEMINI AI
# =============================================================================

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
AI_FEATURES_ENABLED = bool(GEMINI_API_KEY)

# =============================================================================
# 📊 CACHE
# =============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'fitai_cache',
    }
}

# =============================================================================
# 📝 LOGGING
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# =============================================================================
# 🔒 SEGURANÇA
# =============================================================================

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# =============================================================================
# 🎯 INFO
# =============================================================================

if RENDER_EXTERNAL_HOSTNAME:
    print("=" * 60)
    print("🚀 FITAI - PRODUÇÃO")
    print(f"📍 https://{RENDER_EXTERNAL_HOSTNAME}")
    print(f"🗄️  {'PostgreSQL (Neon)' if DATABASE_URL else 'SQLite'}")
    print(f"🔥 Firebase: {'✅' if FIREBASE_CREDENTIALS_JSON else '❌'}")
    print(f"🤖 Gemini: {'✅' if GEMINI_API_KEY else '❌'}")
    print("=" * 60)