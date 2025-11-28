"""
Script de deploy que FORÇA production.py
"""
import os
import sys

#  FORÇA PRODUCTION SETTINGS
os.environ['DJANGO_SETTINGS_MODULE'] = 'fitai.settings.production'

print("\n" + "=" * 80)
print("🔥 DEPLOY SCRIPT - FORÇANDO fitai.settings.production")
print("=" * 80 + "\n")

# Executa o comando do Django
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)