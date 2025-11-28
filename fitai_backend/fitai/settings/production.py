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
# 2. BANCO DE DADOS (CORREÇÃO COMPLETA)
# ==============================================================================
print("🔄 PRODUCTION.PY: Configurando Banco de Dados...")

# Pega a URL do ambiente (SEM strip manual que pode quebrar o parsing)
database_url = os.environ.get('DATABASE_URL', '').strip()

if not database_url:
    print("❌ ERRO CRÍTICO: DATABASE_URL não encontrada!")
    print("   ⚠️  O Render deveria ter definido esta variável automaticamente.")
    print("   💡 Verifique se o PostgreSQL está conectado ao serviço no dashboard do Render.")
    
    # Fallback temporário para não quebrar o import (mas vai falhar no migrate)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Fix para o Render: postgres:// -> postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        print("   ✅ Corrigido: postgres:// → postgresql://")
    
    # Diagnóstico (sem mostrar senha)
    print(f"   📍 URL encontrada (primeiros 40 chars): {database_url[:40]}...")
    
    try:
        # 🔥 MÉTODO CORRETO: Usar dj_database_url.config() diretamente
        # Isso é mais robusto do que parse() manual
        DATABASES = {
            'default': dj_database_url.config(
                default=database_url,
                conn_max_age=600,
                conn_health_checks=True,
                ssl_require=True,
            )
        }
        
        # VALIDAÇÃO FINAL: Verifica se o parsing funcionou
        db_config = DATABASES['default']
        
        if not db_config.get('NAME'):
            print("❌ ERRO: Parsing falhou - NAME está vazio!")
            print(f"   Config resultante: {db_config}")
            raise ValueError("DATABASE_URL parsing falhou - NAME está None")
        
        if db_config.get('HOST') in [None, '', 'localhost', '127.0.0.1']:
            print("❌ ERRO: HOST está incorreto!")
            print(f"   HOST atual: {db_config.get('HOST')}")
            print("   💡 A URL pode estar mal-formada. Exemplo correto:")
            print("   postgresql://user:pass@dpg-xxxxx.oregon-postgres.render.com/dbname")
            raise ValueError("DATABASE_URL parsing falhou - HOST está localhost/None")
        
        # Se chegou aqui, está tudo OK!
        print(f"   ✅ Banco Configurado com Sucesso!")
        print(f"      👉 ENGINE: {db_config.get('ENGINE')}")
        print(f"      👉 HOST:   {db_config.get('HOST')}")
        print(f"      👉 NAME:   {db_config.get('NAME')}")
        print(f"      👉 PORT:   {db_config.get('PORT')}")
        print(f"      👉 SSL:    {db_config.get('OPTIONS', {}).get('sslmode', 'N/A')}")
        
    except Exception as e:
        print(f"❌ ERRO AO CONFIGURAR BANCO: {e}")
        print(f"   DATABASE_URL (mascarada): {database_url[:50]}...")
        raise

# ==============================================================================
# 3. FIREBASE
# ==============================================================================
print("🔥 PRODUCTION.PY: Configurando Firebase...")
FIREBASE_CREDENTIALS_JSON = os.environ.get('FIREBASE_CREDENTIALS_JSON')

if FIREBASE_CREDENTIALS_JSON:
    try:
        clean_json = FIREBASE_CREDENTIALS_JSON.strip().strip("'").strip('"')
        FIREBASE_CONFIG = json.loads(clean_json)
        print("   ✅ Firebase configurado")
    except json.JSONDecodeError as e:
        print(f"   ❌ Erro ao decodificar JSON do Firebase: {e}")
        FIREBASE_CONFIG = None
else:
    print("   ⚠️  FIREBASE_CREDENTIALS_JSON não encontrada")
    FIREBASE_CONFIG = None

# ==============================================================================
# 4. GEMINI AI
# ==============================================================================
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '').strip()
if GEMINI_API_KEY:
    print("   ✅ Gemini API Key encontrada")
    AI_FEATURES_ENABLED = True
else:
    print("   ⚠️  GEMINI_API_KEY não encontrada - IA desabilitada")
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