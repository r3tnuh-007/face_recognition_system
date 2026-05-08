import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


# database.py (continuação)

def inserir_rosto(conn, dados: Dict[str, Any]) -> Optional[int]:
    """
    Insere um novo rosto no banco
    Exemplo de dados: {
        'nome': 'João Silva',
        'nome_arquivo': 'abc123.jpg',
        'caminho_arquivo': 'uploads/faces/2024/01/abc123.jpg',
        'tamanho_arquivo': 1024000,
        'tipo_arquivo': 'image/jpeg',
        'metadados': '{"camera": "iPhone"}'
    }
    """
    query = """
    INSERT INTO rostos (
        nome, nome_arquivo, caminho_arquivo,
        tamanho_arquivo, tipo_arquivo, metadados
    ) VALUES (?, ?, ?, ?, ?, ?)
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query, (
            dados.get('nome'),
            dados['nome_arquivo'],
            dados['caminho_arquivo'],
            dados.get('tamanho_arquivo'),
            dados.get('tipo_arquivo'),
            dados.get('metadados')
        ))
        conn.commit()
        rosto_id = cursor.lastrowid
        print(f"✅ Rosto inserido com ID: {rosto_id}")
        return rosto_id

    except sqlite3.IntegrityError as e:
        print(f"❌ Erro de integridade: {e}")
        return None
    except sqlite3.Error as e:
        print(f"❌ Erro ao inserir: {e}")
        return None

def inserir_log(conn, rosto_id: int, acao: str, ip: str = None,
               user_agent: str = None, detalhes: str = None):
    """Registra log de operação"""
    query = """
    INSERT INTO logs_upload (rosto_id, acao, ip_address, user_agent, detalhes)
    VALUES (?, ?, ?, ?, ?)
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query, (rosto_id, acao, ip, user_agent, detalhes))
        conn.commit()
        print(f"✅ Log registrado para rosto {rosto_id}")
        return True
    except sqlite3.Error as e:
        print(f"❌ Erro ao inserir log: {e}")
        return False

def inserir_multiplos_rostos(conn, lista_rostos: List[Dict]) -> List[int]:
    """Insere múltiplos rostos em lote (mais eficiente)"""
    query = """
    INSERT INTO rostos (
        nome, nome_arquivo, caminho_arquivo,
        tamanho_arquivo, tipo_arquivo, metadados
    ) VALUES (?, ?, ?, ?, ?, ?)
    """

    dados_para_inserir = [
        (
            rosto.get('nome'),
            rosto['nome_arquivo'],
            rosto['caminho_arquivo'],
            rosto.get('tamanho_arquivo'),
            rosto.get('tipo_arquivo'),
            rosto.get('metadados')
        )
        for rosto in lista_rostos
    ]

    try:
        cursor = conn.cursor()
        cursor.executemany(query, dados_para_inserir)
        conn.commit()

        # Recuperar IDs inseridos
        ids = []
        for i in range(len(lista_rostos)):
            ids.append(cursor.lastrowid - len(lista_rostos) + i + 1)

        print(f"✅ Inseridos {len(ids)} rostos em lote")
        return ids

    except sqlite3.Error as e:
        print(f"❌ Erro na inserção em lote: {e}")
        return []
