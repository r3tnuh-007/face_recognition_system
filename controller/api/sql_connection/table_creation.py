import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
from initial_db import *


# database.py (continuação)

def criar_tabela_rostos(conn):
    """Cria tabela de rostos se não existir"""
    query = """
    CREATE TABLE IF NOT EXISTS rostos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        nome_arquivo TEXT NOT NULL UNIQUE,
        caminho_arquivo TEXT NOT NULL,
        tamanho_arquivo INTEGER,
        tipo_arquivo TEXT,
        data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'ativo',
        metadados TEXT,
        embedding TEXT
    )
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("🟢 Tabela 'rostos' criada/verificada com sucesso")
        return True
    except sqlite3.Error as e:
        print(f"☠️ Erro ao criar tabela: {e}")
        return False

def criar_tabela_logs(conn):
    """Cria tabela de logs para auditoria"""
    query = """
    CREATE TABLE IF NOT EXISTS logs_upload (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rosto_id INTEGER,
        acao TEXT NOT NULL,
        ip_address TEXT,
        user_agent TEXT,
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        detalhes TEXT,
        FOREIGN KEY (rosto_id) REFERENCES rostos(id)
    )
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("🟢 Tabela 'logs_upload' criada/verificada com sucesso")
        return True
    except sqlite3.Error as e:
        print(f"☠️ Erro ao criar tabela de logs: {e}")
        return False

def criar_indices(conn):
    """Cria índices para melhor performance"""
    indices = [
        "CREATE INDEX IF NOT EXISTS idx_nome ON rostos(nome)",
        "CREATE INDEX IF NOT EXISTS idx_data_upload ON rostos(data_upload)",
        "CREATE INDEX IF NOT EXISTS idx_status ON rostos(status)",
        "CREATE INDEX IF NOT EXISTS idx_nome_arquivo ON rostos(nome_arquivo)"
    ]

    try:
        cursor = conn.cursor()
        for index in indices:
            cursor.execute(index)
        conn.commit()
        print("🟢 Índices criados com sucesso")
        return True
    except sqlite3.Error as e:
        print(f"☠️ Erro ao criar índices: {e}")
        return False

def inicializar_banco():
    """Inicializa todas as tabelas e índices"""
    conn = conectar_banco()
    if not conn:
        return False

    criar_tabela_rostos(conn)
    criar_tabela_logs(conn)
    criar_indices(conn)

    fechar_banco(conn)
    return True
