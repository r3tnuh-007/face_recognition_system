import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
from  sql_connection.initial_db import *


# CREATE TABLES

def create_table_images(conn):
    """Cria tabela de imagens se não existir"""
    query = """
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        user_email TEXT NOT NULL,
        nome_arquivo TEXT NOT NULL UNIQUE,
        data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'useless'
    )
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("🟢 Tabela 'images' criada/verificada com sucesso")
        return True
    except sqlite3.Error as e:
        print(f"☠️ Erro ao criar tabela: {e}")
        return False


def create_table_matched(conn):
    """Cria tabela de matches se não existir"""
    query = """
    CREATE TABLE IF NOT EXISTS matched (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email_user_lost TEXT NOT NULL,
		email_user_found TEXT NOT NULL,
        nome_arquivo_lost TEXT NOT NULL,
        nome_arquivo_found TEXT NOT NULL,
        data_match TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("🟢 Tabela 'matched' criada/verificada com sucesso")
        return True
    except sqlite3.Error as e:
        print(f"☠️ Erro ao criar tabela: {e}")
        return False


def create_table_users(conn):
    """Cria tabela de logs para auditoria"""
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT NOT NULL UNIQUE,
        contact TEXT NOT NULL UNIQUE,
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("🟢 Tabela 'users' criada/verificada com sucesso")
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
    conn = connect_db()
    if not conn:
        return False
    create_table_images(conn)
    create_table_users(conn)
    close_db(conn)
    return True
