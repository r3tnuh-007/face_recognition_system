# main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status, Request
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import shutil
import uuid
from typing import Optional
import aiofiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from utils import listar, face_check, valid_image
import os
from mangum import Mangum

from sql_connection.insert_function import *
from sql_connection.initial_db import *
from sql_connection.table_creation import *
from sql_connection.consult_function import *

from utils.face_search import *

app = FastAPI(
    title="API de Alta Performance",
    version="1.0.0"
)

origin = [
    "http://localhost:8000",
    "http://localhost:4242",
    "http://canned-tainted-washstand.ngrok-free.dev",
    "https://canned-tainted-washstand.ngrok-free.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],		# Quais sites podem chamar sua API
    allow_credentials=True,		# Permite cookies/auth headers
    allow_methods=["*"],		# Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],		# Permite todos os headers
)


# Configurações
UPLOAD_DIR = Path("img")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

@app.get("/")
async def home():
    return {"mensagem": "Face recognition rodando com alta performance!",
            "Owner": "r3tnuh-007 Ice heart"
            }


@app.get("/images/{caminho_completo:path}")
async def servir_imagem_simples(caminho_completo: str):
    """
    Endpoint mais flexível para servir imagens
    Exemplo: /images/lost/2026/05/foto.jpg
    """
    # Garantir que só acessa a pasta img
    if '..' in caminho_completo:
        raise HTTPException(status_code=403, detail="Caminho inválido")
    caminho_arquivo = os.path.join("img/", caminho_completo)
    if not os.path.exists(caminho_arquivo):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    # Determinar media type
    extensao = os.path.splitext(caminho_arquivo)[1].lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    return FileResponse(
        caminho_arquivo,
        media_type=media_types.get(extensao, 'application/octet-stream')
    )


@app.post("/dashboard")
async def faces_dashboard():
    absolute = "img/"
    try:
        #arquivos = listar.listar_arquivos(absolute)
        conn = connect_db()
        img_lost = search_faces(conn, status="lost")
        print(f"img_lost: {img_lost}")
        close_db(conn)
    except:
        print("Caminho invalido")
    id = 0
    result = []
    base_url = "http://10.18.32.206:4242/"
    for img in img_lost:
        result.append(
            {
                "id": img['id'],
                "nome": img['nome'],
                "imageUrl": base_url + "images/" + img['nome_arquivo'],
                "status": img['status'],
                "data_upload": img['data_upload'],
                "user_email": img['user_email']
            })
        id += 1
    print(f"TIME:	  {datetime.now().strftime('%Hh%Mm%Ss.%f')}")
    return result


@app.post("/faces/search")
async def search_face(
    imagem: UploadFile = File(..., description="Arquivo de imagem do rosto")
    ):
    """
    Endpoint para upload de imagem de rosto
    """
    try:
        # Validar tamanho (verificar headers primeiro)
        if hasattr(imagem, 'size') and imagem.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"Arquivo muito grande! Máximo: {MAX_FILE_SIZE // 1024 // 1024}MB"
            )
        # Validar tipo de arquivo
        if not valid_image.validar_imagem(imagem):
            raise HTTPException(
            status_code=400,
            detail=f"Extensão não permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        # Criar estrutura de pastas por data
        pasta_data = UPLOAD_DIR
        # Gerar nome único
        extensao = Path(imagem.filename).suffix.lower()
        nome = "Unknown_found"
        nome_base = nome.replace(" ", "_") if nome else "rosto"
        nome_unico = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nome_base}_{uuid.uuid4().hex[:8]}{extensao}"
        # Caminho final
        caminho_imagem = pasta_data / nome_unico
        # Salvar imagem com aiofiles (assíncrono)
        async with aiofiles.open(caminho_imagem, 'wb') as buffer:
            conteudo = await imagem.read()
            # Verificar tamanho após leitura
            if len(conteudo) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    message="Arquivo excede o tamanho máximo permitido"
                )
            await buffer.write(conteudo)
        # Retornar resposta de sucesso
        conn = connect_db()
        data = {
            "nome": nome,
            "nome_arquivo": nome_unico,
            "user_email": "anterofranciso@gmail.com",
            "status": "found"
        }
        insert_image(conn, data)
        face =  await face_check.check_face(str(caminho_imagem))
        if (not face):
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Face not detected"
                }
            )
        imgs = search_faces(conn, status="lost")
        print(imgs)
        try:
            re = await task_builder(str(caminho_imagem), array)
            print(re)
        except:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Something went wrong with the photo"
                }
            )
        data = []
        base_url = "http://10.18.32.206:4242/"
        for img in re:
            if img[0]:
                img_lost = search_face_by_filename(conn, img[1])
                print(f"detalhes da imagem: {img_lost}")
                data.append({
                    "message": "🟢 Pessoa encontrada com sucesso!",
                    "id": img_lost['id'],
                    "nome": img_lost['nome'],
                    "arquivo": img[1],
                    "imageUrl": base_url + "images/" + img[1],
                    "tamanho": len(conteudo),
                    "tipo": imagem.content_type,
                    "data_upload": img_lost['data_upload'],
                    "similarity": 0.96,
                    "user_email": img_lost['user_email']
                })
        close_db(conn)
        return JSONResponse(
            status_code=201,
            content=data
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            message=f"Erro interno ao processar upload: {str(e)}"
        )


@app.post("/faces")
async def publicar_rosto(
    imagem: UploadFile = File(..., description="Arquivo de imagem do rosto"),
    nome: Optional[str] = Form(None, description="Nome opcional da pessoa")
    ):
    """
    Endpoint para upload de imagem de rosto
    """
    try:
        # Validar tamanho (verificar headers primeiro)
        if hasattr(imagem, 'size') and imagem.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"Arquivo muito grande! Máximo: {MAX_FILE_SIZE // 1024 // 1024}MB"
            )
        # Validar tipo de arquivo
        if not valid_image.validar_imagem(imagem):
            raise HTTPException(
            status_code=400,
            detail=f"Extensão não permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        # Criar estrutura de pastas por data
        pasta_data = UPLOAD_DIR
        # Gerar nome único
        extensao = Path(imagem.filename).suffix.lower()
        nome_base = nome.replace(" ", "_") if nome else "rosto"
        nome_unico = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nome_base}_{uuid.uuid4().hex[:8]}{extensao}"
        # Caminho final
        caminho_imagem = pasta_data / nome_unico
        # Salvar imagem com aiofiles (assíncrono)
        async with aiofiles.open(caminho_imagem, 'wb') as buffer:
            conteudo = await imagem.read()
            # Verificar tamanho após leitura
            if len(conteudo) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail="Arquivo excede o tamanho máximo permitido"
                )
            await buffer.write(conteudo)
        # Retornar resposta de sucesso
        #caminho_image = str(caminho_imagem)
        face =  await face_check.check_face(caminho_imagem)
        if (not face):
            return JSONResponse(
                status_code=400,
                content={
                "message": "Face not detected"
            })
        if nome == None:
            nome = "Unknown"
        print(f"🟢 {nome}, {nome_unico}, {str(caminho_imagem)}, {len(conteudo)}, {imagem.content_type}")
        conn = connect_db()
        dados_imagem = {
            'nome': nome,
            'user_email': 'anterofranciso@gmail.com',
            'nome_arquivo': nome_unico,
            "status": "lost"
        }
        data = insert_image(conn, dados_imagem)
        if(not data):
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Erro ao publicar rosto"
                }
            )
        close_db(conn)
        return JSONResponse(
            status_code=201,
            content={
                "message": "🟢 Rosto publicado com sucesso!",
                "tipo": imagem.content_type,
                "data_upload": datetime.now().isoformat(),
                "similarity": 0.9
            }
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar upload: {str(e)}"
        )


@app.post("/faces")
async def publicar_rosto(
    imagem: UploadFile = File(..., description="Arquivo de imagem do rosto"),
    nome: Optional[str] = Form(None, description="Nome opcional da pessoa")
    ):
    """
    Endpoint para upload de imagem de rosto
    """
    try:
        # Validar tamanho (verificar headers primeiro)
        if hasattr(imagem, 'size') and imagem.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"Arquivo muito grande! Máximo: {MAX_FILE_SIZE // 1024 // 1024}MB"
            )
        # Validar tipo de arquivo
        if not valid_image.validar_imagem(imagem):
            raise HTTPException(
            status_code=400,
            detail=f"Extensão não permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        # Criar estrutura de pastas por data
        pasta_data = UPLOAD_DIR
        # Gerar nome único
        extensao = Path(imagem.filename).suffix.lower()
        nome_base = nome.replace(" ", "_") if nome else "rosto"
        nome_unico = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nome_base}_{uuid.uuid4().hex[:8]}{extensao}"
        # Caminho final
        caminho_imagem = pasta_data / nome_unico
        # Salvar imagem com aiofiles (assíncrono)
        async with aiofiles.open(caminho_imagem, 'wb') as buffer:
            conteudo = await imagem.read()
            # Verificar tamanho após leitura
            if len(conteudo) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail="Arquivo excede o tamanho máximo permitido"
                )
            await buffer.write(conteudo)
        # Retornar resposta de sucesso
        #caminho_image = str(caminho_imagem)
        face =  await face_check.check_face(caminho_imagem)
        if (not face):
            return JSONResponse(
                status_code=400,
                content={
                "message": "Face not detected"
            })
        if nome == None:
            nome = "Unknown"
        print(f"🟢 {nome}, {nome_unico}, {str(caminho_imagem)}, {len(conteudo)}, {imagem.content_type}")
        conn = connect_db()
        dados_imagem = {
            'nome': nome,
            'user_email': 'anterofranciso@gmail.com',
            'nome_arquivo': nome_unico,
            "status": "lost"
        }
        data = insert_image(conn, dados_imagem)
        if(not data):
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Erro ao publicar rosto"
                }
            )
        close_db(conn)
        return JSONResponse(
            status_code=201,
            content={
                "message": "🟢 Rosto publicado com sucesso!",
                "data": {
                    "nome": nome,
                    "arquivo": nome_unico,
                    "caminho": str(caminho_imagem),
                    "tamanho": len(conteudo),
                    "tipo": imagem.content_type,
                    "data_upload": datetime.now().isoformat()
                }
            }
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar upload: {str(e)}"
        )


@app.get("/faces/{nome_arquivo}")
async def obter_imagem(nome_arquivo: str):
    """
    Retorna uma imagem salva
    """
    # Buscar em toda estrutura de pastas
    for caminho in UPLOAD_DIR.rglob(nome_arquivo):
        if caminho.is_file():
            return FileResponse(
                caminho,
                media_type=f"image/{caminho.suffix[1:]}",
                filename=caminho.name
            )
    raise HTTPException(status_code=404, detail="Imagem não encontrada")


@app.get("/health")
async def health_check():
    return {"status": "ok", "server": "uvicorn"}

handler = Mangum(app)

__all__ = ['app', 'handler']
