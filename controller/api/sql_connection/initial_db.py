# database.py
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

# Configuração global
DB_NAME = "rostos_fastapi.db"  # Nome do banco de dados

def conectar_banco():
    """Estabelece conexão com o banco de dados"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        print(f"✅ Conectado ao banco: {DB_NAME}")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def fechar_banco(conn):
    """Fecha conexão com o banco"""
    if conn:
        conn.close()
        print("🔒 Conexão fechada")
