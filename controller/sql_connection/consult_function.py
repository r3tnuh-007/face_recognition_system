import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


# QUERIES

def search_faces(conn, status="useless") -> List[Dict]:
    """Retorna todos os rostos cadastrados"""
    query = "SELECT * FROM images WHERE status = ? ORDER BY data_upload DESC"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (status,))
        resultados = cursor.fetchall()
        return [dict(row) for row in resultados]
    except sqlite3.Error as e:
        print(f"🚫 Erro na consulta: {e}")
        return []


def search_face_by_id(conn, face_id: int) -> Optional[Dict]:
    """Busca rosto pelo ID"""
    query = "SELECT * FROM images WHERE id = ? AND status = 'ativo'"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (face_id,))
        resultado = cursor.fetchone()
        return dict(resultado) if resultado else None
    except sqlite3.Error as e:
        print(f"🚫 Erro na consulta: {e}")
        return None


def search_user(conn, user_email: str) -> Optional[Dict]:
    """Busca usuário pelo email"""
    query = "SELECT * FROM users WHERE email = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (user_email,))
        resultado = cursor.fetchone()
        return dict(resultado) if resultado else None
    except sqlite3.Error as e:
        print(f"🚫 Erro na consulta: {e}")
        return None


def search_face_by_filename(conn, filename: str) -> Optional[Dict]:
    """Busca rosto pelo nome do arquivo"""
    query = "SELECT * FROM images WHERE nome_arquivo = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (filename,))
        resultado = cursor.fetchone()
        return dict(resultado) if resultado else None
    except sqlite3.Error as e:
        print(f"🚫 Erro na consulta: {e}")
        return None


def search_face_by_name(conn, name: str) -> List[Dict]:
    """Busca rostos por nome (busca parcial)"""
    query = "SELECT * FROM images WHERE nome = ? AND status = 'ativo'"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (f"%{name}%",))
        resultados = cursor.fetchall()
        return [dict(row) for row in resultados]
    except sqlite3.Error as e:
        print(f"🚫 Erro na consulta: {e}")
        return []


def delete_face(conn, face_id: int, logical: bool = True) -> bool:
    """
    Deleta um rosto
    logical=True: apenas marca como matched (soft delete)
    logical=False: remove permanentemente
    """
    if logical:
        query = "UPDATE images SET status = 'matched' WHERE id = ?"
    else:
        query = "DELETE FROM images WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (face_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"🟢 Rosto {face_id} {'marcado como matched' if logical else 'removido'} com sucesso")
            return True
        else:
            print(f"🚫 Rosto {face_id} não encontrado")
            return False
    except sqlite3.Error as e:
        print(f"🚫 Erro ao deletar: {e}")
        return False
