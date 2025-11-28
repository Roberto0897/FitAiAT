"""
Configurações de Produção para o Render.
Arquivo BLINDADO: Limpa a URL do banco antes de conectar.
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
SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-temporaria-para-build-segura')
DEBUG = False

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
ALLOWED_HOSTS.append('.onrender.com')

# ==============================================================================
# 2. BANCO DE DADOS (CORREÇÃO DE LIMPEZA DE STRING)
# ==============================================================================
print("🔄 PRODUCTION.PY: Configurando Banco de Dados...")

# Pega a URL bruta
raw_db_url = os.environ.get('DATABASE_URL', '')

# 🔥 LIMPEZA PROFUNDA: Remove espaços, aspas simples e duplas que podem quebrar o parser
database_url = raw_db_url.strip().strip('"').strip("'")

if database_url:
    # Fix para o Render (postgres:// -> postgresql://)
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    # Diagnóstico da URL (Sem mostrar a senha)
    print(f"   URL Bruta (Tamanho): {len(raw_db_url)}")
    print(f"   URL Limpa (Tamanho): {len(database_url)}")
    
    try:
        # Configura o DATABASES
        db_config = dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
        
        DATABASES = {
            'default': db_config
        }
        
        # VERIFICAÇÃO FINAL
        if DATABASES['default'].get('NAME') is None:
             print("❌ ERRO: O 'NAME' do banco está vazio! A URL pode estar incompleta.")
        
        print(f"✅ PRODUCTION.PY: Banco Configurado!")
        print(f"   👉 Host: {DATABASES['default'].get('HOST')}")
        print(f"   👉 Name: {DATABASES['default'].get('NAME')}")
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO AO CONFIGURAR BANCO: {e}")
        raise e
else:
    print("❌ PRODUCTION.PY: DATABASE_URL não encontrada ou vazia!")
    # Fallback para SQLite para não quebrar o import, mas vai falhar no migrate
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
        # Limpa também o JSON por precaução
        clean_json = FIREBASE_CREDENTIALS_JSON.strip().strip("'").strip('"')
        FIREBASE_CONFIG = json.loads(clean_json)
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
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '').strip()
if GEMINI_API_KEY:
    print("✅ Gemini API Key encontrada")
    AI_FEATURES_ENABLED = True
else:
    print("⚠️  GEMINI_API_KEY não encontrada")
    AI_FEATURES_ENABLED = False

# ==============================================================================
# 5. SEGURANÇA WEB & ESTÁTICOS
# ==============================================================================
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

print("=" * 80 + "\n")