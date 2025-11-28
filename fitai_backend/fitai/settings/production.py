"""
Configurações de Produção - HARDCODED
"""
from .base import *
import dj_database_url
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
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True,
    )
}

# Debug para confirmar
db = DATABASES['default']
print(f"🗄️  HOST: {db.get('HOST', 'N/A')}")
print(f"🗄️  NAME: {db.get('NAME', 'N/A')}")

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