"""
Objetivo: Mostrar EXATAMENTE o que o Django está carregando.
"""
import os
import sys
import django
from django.conf import settings

# 1. FORÇA A CONFIGURAÇÃO DE PRODUÇÃO
os.environ['DJANGO_SETTINGS_MODULE'] = 'fitai.settings.production'

print("\n" + "█" * 80)
print("🕵️ INICIANDO INSPEÇÃO DO AMBIENTE")
print("█" * 80)

# 2. VERIFICA A VARIÁVEL DE AMBIENTE DATABASE_URL
db_url = os.environ.get('DATABASE_URL')
if db_url:
    print(f"✅ ENV['DATABASE_URL']: Encontrada!")
    print(f"   Valor (oculto): {db_url[:15]}...******")
else:
    print("❌ ENV['DATABASE_URL']: NÃO ENCONTRADA! O Render não passou a URL do banco.")

# 3. CARREGA O DJANGO PARA VER A CONFIGURAÇÃO FINAL
try:
    django.setup()
    print("\n✅ Django carregado com sucesso.")
    
    # PEGA A CONFIGURAÇÃO REAL DO BANCO
    db_settings = settings.DATABASES['default']
    
    print("\n🧐 CONFIGURAÇÃO DO BANCO CARREGADA (settings.DATABASES):")
    print(f"   👉 ENGINE: {db_settings.get('ENGINE')}")
    print(f"   👉 HOST:   {db_settings.get('HOST')}")
    print(f"   👉 NAME:   {db_settings.get('NAME')}")
    print(f"   👉 PORT:   {db_settings.get('PORT')}")
    
    print("\n📂 ARQUIVO DE SETTINGS USADO:")
    print(f"   {os.environ.get('DJANGO_SETTINGS_MODULE')}")

except Exception as e:
    print(f"\n❌ CRASH AO CARREGAR DJANGO: {e}")

print("█" * 80 + "\n")

# 4. EXECUTA O COMANDO ORIGINAL (COM A FLAG --settings)
from django.core.management import execute_from_command_line

# Garante que a flag --settings está presente
if '--settings=fitai.settings.production' not in sys.argv:
    sys.argv.append('--settings=fitai.settings.production')

print("🚀 Executando comando...")
execute_from_command_line(sys.argv)