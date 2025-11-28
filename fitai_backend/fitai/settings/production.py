from .base import *
import os
import json
from urllib.parse import urlparse

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
# 2. BANCO DE DADOS (PARSE MANUAL - SEM DJ-DATABASE-URL)
# ==============================================================================
print("🔄 PRODUCTION.PY: Configurando Banco de Dados...")

database_url = os.environ.get('DATABASE_URL', '').strip()

if not database_url:
    print("❌ ERRO CRÍTICO: DATABASE_URL não encontrada!")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    print(f"   📍 URL encontrada (primeiros 50 chars): {database_url[:50]}...")
    
    # Fix Render: postgres:// -> postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        print("   ✅ Corrigido: postgres:// → postgresql://")
    
    try:
        # 🔥 PARSE MANUAL com urllib.parse (não depende de dj-database-url)
        parsed = urlparse(database_url)
        
        # Extrai os componentes
        db_name = parsed.path.replace('/', '')  # Remove a barra inicial
        db_user = parsed.username
        db_password = parsed.password
        db_host = parsed.hostname
        db_port = parsed.port or 5432
        
        print(f"\n   📊 Componentes parseados:")
        print(f"      Scheme:   {parsed.scheme}")
        print(f"      Host:     {db_host}")
        print(f"      Port:     {db_port}")
        print(f"      Database: {db_name}")
        print(f"      User:     {db_user}")
        
        # Validações críticas
        if not db_host or db_host in ['localhost', '127.0.0.1']:
            print(f"\n   ❌ ERRO: HOST inválido: {db_host}")
            raise ValueError(f"HOST inválido: {db_host}")
        
        if not db_name:
            print(f"\n   ❌ ERRO: Database name está vazio!")
            raise ValueError("Database name está vazio")
        
        if not db_user:
            print(f"\n   ❌ ERRO: Username está vazio!")
            raise ValueError("Username está vazio")
        
        # 🎯 CONFIGURAÇÃO MANUAL DO DATABASES (bypassa dj-database-url completamente)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_password,
                'HOST': db_host,
                'PORT': db_port,
                'OPTIONS': {
                    'sslmode': 'require',
                },
                'CONN_MAX_AGE': 600,
                'CONN_HEALTH_CHECKS': True,
            }
        }
        
        print(f"\n   ✅ Banco Configurado Manualmente!")
        print(f"      ENGINE: {DATABASES['default']['ENGINE']}")
        print(f"      HOST:   {DATABASES['default']['HOST']}")
        print(f"      NAME:   {DATABASES['default']['NAME']}")
        print(f"      PORT:   {DATABASES['default']['PORT']}")
        
    except Exception as e:
        print(f"\n   ❌ ERRO AO CONFIGURAR BANCO: {e}")
        print(f"   DATABASE_URL problemática: {database_url[:60]}...")
        
        # Debug adicional
        try:
            test_parse = urlparse(database_url)
            print(f"\n   🔍 Debug urllib.parse:")
            print(f"      scheme:   '{test_parse.scheme}'")
            print(f"      netloc:   '{test_parse.netloc}'")
            print(f"      hostname: '{test_parse.hostname}'")
            print(f"      port:     {test_parse.port}")
            print(f"      path:     '{test_parse.path}'")
            print(f"      username: '{test_parse.username}'")
        except Exception as parse_error:
            print(f"   ❌ Erro no debug: {parse_error}")
        
        raise

# ==============================================================================
# 3. FIREBASE
# ==============================================================================
print("\n🔥 PRODUCTION.PY: Configurando Firebase...")
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