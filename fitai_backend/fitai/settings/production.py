"""
Configurações de Produção para o Render.
Arquivo COMPLETO: Banco de Dados + Firebase + Gemini + Segurança.
"""
from .base import *
import os
import json
import dj_database_url

print("\n" + "=" * 80)
print("🚀 PRODUCTION.PY: Carregando configurações...")

# ==============================================================================
# 1. SEGURANÇA BÁSICA
# ==============================================================================
# Se não houver SECRET_KEY, usa uma temporária para o build não falhar
SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-temporaria-para-build-segura')
DEBUG = False

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
ALLOWED_HOSTS.append('.onrender.com')

# ==============================================================================
# 2. BANCO DE DADOS (A CORREÇÃO ESTÁ AQUI!)
# ==============================================================================
print("🔄 PRODUCTION.PY: Configurando Banco de Dados...")

database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Fix para o Render (postgres:// -> postgresql://)
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    # Configura o DATABASES usando parse com flags de segurança OBRIGATÓRIAS
    try:
        db_config = dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,  # 🔥 ESSENCIAL PARA O RENDER
        )
        DATABASES = {
            'default': db_config
        }
        print(f"✅ PRODUCTION.PY: Banco Configurado!")
        print(f"   👉 Host: {DATABASES['default'].get('HOST')}")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO AO CONFIGURAR BANCO: {e}")
        # Não fazemos fallback para SQLite aqui para forçar o erro aparecer se falhar
        raise e
else:
    print("❌ PRODUCTION.PY: DATABASE_URL não encontrada! O site vai quebrar.")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==============================================================================
# 3. FIREBASE
# ==============================================================================
print("🔥 PRODUCTION.PY: Configurando Firebase...")
FIREBASE_CREDENTIALS_JSON = os.environ.get('FIREBASE_CREDENTIALS_JSON')

if FIREBASE_CREDENTIALS_JSON:
    try:
        FIREBASE_CONFIG = json.loads(FIREBASE_CREDENTIALS_JSON)
        print("✅ Firebase configurado com sucesso")
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON do Firebase: {e}")
        FIREBASE_CONFIG = None
else:
    print("⚠️  FIREBASE_CREDENTIALS_JSON não encontrada")
    FIREBASE_CONFIG = None

# ==============================================================================
# 4. GEMINI AI
# ==============================================================================
print("🤖 PRODUCTION.PY: Configurando Gemini...")
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    print("✅ Gemini API Key encontrada")
    AI_FEATURES_ENABLED = True
else:
    print("⚠️  GEMINI_API_KEY não encontrada")
    AI_FEATURES_ENABLED = False

# ==============================================================================
# 5. SEGURANÇA WEB (HTTPS & CORS)
# ==============================================================================
# Redireciona tudo para HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ==============================================================================
# 6. ARQUIVOS ESTÁTICOS (WhiteNoise)
# ==============================================================================
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

print("=" * 80 + "\n")