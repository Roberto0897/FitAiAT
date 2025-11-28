"""
Configurações de Produção - HARDCODED
"""
from .base import *
import os

# =============================================================================
# 🔒 SEGURANÇA
# =============================================================================
DEBUG = False
ALLOWED_HOSTS = ['.onrender.com', 'fitaiat.onrender.com']
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# =============================================================================
# 🗄️ BANCO DE DADOS - HARDCODED DIRETO
# =============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fitai_database',
        'USER': 'fitai_user',
        'PASSWORD': 'jK8Wcb6w75UvLYQ1nsTd1fyBKHovOifG',
        'HOST': 'dpg-d4kea0euk2gs73fq5nqg-a.oregon-postgres.render.com',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

print("=" * 80)
print("🗄️  BANCO: PostgreSQL Render (HARDCODED)")
print(f"    HOST: {DATABASES['default']['HOST']}")
print(f"    NAME: {DATABASES['default']['NAME']}")
print("=" * 80)

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
import json
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