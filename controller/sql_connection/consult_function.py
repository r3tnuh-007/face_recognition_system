import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


# Consultas GET

def buscar_todos_rostos(conn) -> List[Dict]:
    """Retorna todos os rostos cadastrados"""
    query = "SELECT * FROM rostos WHERE status = 'ativo' ORDER BY data_upload DESC"

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        return [dict(row) for row in resultados]
    except sqlite3.Error as e:
        print(f"❌ Erro na consulta: {e}")
        return []

def buscar_rosto_por_id(conn, rosto_id: int) -> Optional[Dict]:
    """Busca rosto pelo ID"""
    query = "SELECT * FROM rostos WHERE id = ? AND status = 'ativo'"

    try:
        cursor = conn.cursor()
        cursor.execute(query, (rosto_id,))
        resultado = cursor.fetchone()
        return dict(resultado) if resultado else None
    except sqlite3.Error as e:
        print(f"❌ Erro na consulta: {e}")
        return None

def buscar_rosto_por_nome_arquivo(conn, nome_arquivo: str) -> Optional[Dict]:
    """Busca rosto pelo nome do arquivo"""
    query = "SELECT * FROM rostos WHERE nome_arquivo = ?"

    try:
        cursor = conn.cursor()
        cursor.execute(query, (nome_arquivo,))
        resultado = cursor.fetchone()
        return dict(resultado) if resultado else None
    except sqlite3.Error as e:
        print(f"❌ Erro na consulta: {e}")
        return None

def buscar_por_nome(conn, nome: str) -> List[Dict]:
    """Busca rostos por nome (busca parcial)"""
    query = "SELECT * FROM rostos WHERE nome LIKE ? AND status = 'ativo'"

    try:
        cursor = conn.cursor()
        cursor.execute(query, (f"%{nome}%",))
        resultados = cursor.fetchall()
        return [dict(row) for row in resultados]
    except sqlite3.Error as e:
        print(f"❌ Erro na consulta: {e}")
        return []

def buscar_logs_por_rosto(conn, rosto_id: int) -> List[Dict]:
    """Busca logs de um rosto específico"""
    query = """
    SELECT * FROM logs_upload
    WHERE rosto_id = ?
    ORDER BY data_hora DESC
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query, (rosto_id,))
        resultados = cursor.fetchall()
        return [dict(row) for row in resultados]
    except sqlite3.Error as e:
        print(f"❌ Erro na consulta de logs: {e}")
        return []

def contar_rostos(conn) -> int:
    """Conta total de rostos cadastrados"""
    query = "SELECT COUNT(*) as total FROM rostos WHERE status = 'ativo'"

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        return resultado['total'] if resultado else 0
    except sqlite3.Error as e:
        print(f"❌ Erro ao contar: {e}")
        return 0


# Consultas UPDATE e DELETE
def atualizar_nome_rosto(conn, rosto_id: int, novo_nome: str) -> bool:
    """Atualiza o nome de um rosto"""
    query = """
    UPDATE rostos
    SET nome = ?, data_atualizacao = CURRENT_TIMESTAMP
    WHERE id = ? AND status = 'ativo'
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query, (novo_nome, rosto_id))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Nome do rosto {rosto_id} atualizado para '{novo_nome}'")
            return True
        else:
            print(f"❌ Rosto {rosto_id} não encontrado")
            return False
    except sqlite3.Error as e:
        print(f"❌ Erro ao atualizar: {e}")
        return False

def deletar_rosto(conn, rosto_id: int, logico: bool = True) -> bool:
    """
    Deleta um rosto
    logico=True: apenas marca como inativo (soft delete)
    logico=False: remove permanentemente
    """
    if logico:
        query = "UPDATE rostos SET status = 'inativo' WHERE id = ?"
    else:
        query = "DELETE FROM rostos WHERE id = ?"

    try:
        cursor = conn.cursor()
        cursor.execute(query, (rosto_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Rosto {rosto_id} {'desativado' if logico else 'removido'} com sucesso")
            return True
        else:
            print(f"❌ Rosto {rosto_id} não encontrado")
            return False
    except sqlite3.Error as e:
        print(f"❌ Erro ao deletar: {e}")
        return False
