import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
from sql_connection.table_creation import *


# INSERT INFO

def insert_image(conn, dados: Dict[str, Any]) -> Optional[int]:
    """
    Insere uma nova imagem no banco
    Exemplo de dados: {
        'nome': 'João Silva',
        'nome_arquivo': 'abc123.jpg',
        'caminho_arquivo': 'uploads/faces/2024/01/abc123.jpg',
        'tamanho_arquivo': 1024000,
        'tipo_arquivo': 'image/jpeg',
        'metadados': '{"camera": "iPhone"}'
    }
    """
    create_table_images(conn)  # Garantir que a tabela exista antes de inserir
    query = """
    INSERT INTO images (
        nome, user_email, nome_arquivo, status
    ) VALUES (?, ?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, (
            dados['nome'],
            dados['user_email'],
            dados['nome_arquivo'],
            dados['status']
        ))
        conn.commit()
        rosto_id = cursor.lastrowid
        print(f"🟢 Rosto inserido com ID: {rosto_id}")
        return rosto_id
    except sqlite3.IntegrityError as e:
        print(f"🚫 Erro de integridade: {e}")
        return None
    except sqlite3.Error as e:
        print(f"🚫 Erro ao inserir: {e}")
        return None

def insert_match(conn, dados: Dict[str, Any]) -> Optional[int]:
    """
    Insere um novo match no banco
    Exemplo de dados: {
        'nome_arquivo_lost': 'abc123.jpg',
        'nome_arquivo_found': 'xyz456.jpg'
    }
    """
    create_table_matched(conn)  # Garantir que a tabela exista antes de inserir
    query = """
    INSERT INTO matched (
        nome, email_user_lost, email_user_found, nome_arquivo_lost, nome_arquivo_found
    ) VALUES (?, ?, ?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, (
            dados['nome'],
            dados['email_user_lost'],
            dados['email_user_found'],
            dados['nome_arquivo_lost'],
            dados['nome_arquivo_found']
        ))
        conn.commit()
        match_id = cursor.lastrowid
        print(f"🟢 Match inserido com ID: {match_id}")
        return match_id
    except sqlite3.IntegrityError as e:
        print(f"🚫 Erro de integridade: {e}")
        return None
    except sqlite3.Error as e:
        print(f"🚫 Erro ao inserir: {e}")
        return None


def insert_user(conn, dados: Dict[str, Any]) -> Optional[int]:
    """
    Insere um novo usuário no banco
    Exemplo de dados: {
        'nome': 'João Silva',
        'email': 'joao@example.com',
        'contact': '123456789',
    }
    """
    create_table_users(conn)  # Garantir que a tabela exista antes de inserir
    query = """
    INSERT INTO users (
        nome, email, contact
    ) VALUES (?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, (
            dados['nome'],
            dados['email'],
            dados['contact']
        ))
        conn.commit()
        user_id = cursor.lastrowid
        print(f"🟢 Usuário inserido com ID: {user_id}")
        return user_id
    except sqlite3.IntegrityError as e:
        print(f"🚫 Erro de integridade: {e}")
        return None
    except sqlite3.Error as e:
        print(f"🚫 Erro ao inserir: {e}")
        return None
