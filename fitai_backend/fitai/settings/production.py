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
# 2. BANCO DE DADOS (FIX DEFINITIVO)
# ==============================================================================
print("🔄 PRODUCTION.PY: Configurando Banco de Dados...")

# Pega a URL do ambiente
database_url = os.environ.get('DATABASE_URL', '').strip()

if not database_url:
    print("❌ ERRO CRÍTICO: DATABASE_URL não encontrada!")
    print("   💡 Conecte o PostgreSQL no dashboard do Render")
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Fix Render: postgres:// -> postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        print("   ✅ Corrigido: postgres:// → postgresql://")
    
    print(f"   📍 URL encontrada (primeiros 50 chars): {database_url[:50]}...")
    
    try:
        # 🔥 FIX: Usa parse() em vez de config()
        # config() busca do ambiente, parse() usa a string que passamos
        db_config = dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
        
        print(f"\n   📊 Resultado do parse:")
        print(f"      ENGINE: {db_config.get('ENGINE')}")
        print(f"      HOST:   {db_config.get('HOST')}")
        print(f"      NAME:   {db_config.get('NAME')}")
        print(f"      USER:   {db_config.get('USER')}")
        print(f"      PORT:   {db_config.get('PORT')}")
        
        # Validações críticas
        if not db_config.get('NAME'):
            print("\n   ❌ ERRO: NAME está vazio após parse!")
            print(f"   DATABASE_URL pode estar mal-formada")
            print(f"   Formato correto: postgresql://user:pass@host.com:5432/dbname")
            raise ValueError("DATABASE_URL parsing falhou - NAME está None")
        
        if db_config.get('HOST') in [None, '', 'localhost', '127.0.0.1']:
            print("\n   ❌ ERRO: HOST está incorreto!")
            print(f"   HOST parseado: {db_config.get('HOST')}")
            print(f"   DATABASE_URL está incompleta ou inválida")
            raise ValueError("DATABASE_URL parsing falhou - HOST inválido")
        
        # Configura o DATABASES
        DATABASES = {'default': db_config}
        
        print(f"\n   ✅ Banco Configurado com Sucesso!")
        
    except Exception as e:
        print(f"\n   ❌ ERRO AO CONFIGURAR BANCO: {e}")
        print(f"   DATABASE_URL (mascarada): {database_url[:60]}...")
        
        # Se falhar, mostra a URL completa (mascarando senha)
        try:
            from urllib.parse import urlparse
            parsed = urlparse(database_url)
            print(f"\n   🔍 Debug da URL:")
            print(f"      Scheme: {parsed.scheme}")
            print(f"      Host: {parsed.hostname}")
            print(f"      Port: {parsed.port}")
            print(f"      Path (dbname): {parsed.path}")
            print(f"      User: {parsed.username}")
        except:
            pass
        
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
