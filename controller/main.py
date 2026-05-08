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
from utils import listar, face_check

app = FastAPI(
    title="API de Alta Performance",
    version="1.0.0"
)

origin = [
    "http://localhost:8000",
    "http://localhost:4242",
    "http://canned-tainted-washstand.ngrok-free.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],		# Quais sites podem chamar sua API
    allow_credentials=False,	# Permite cookies/auth headers
    allow_methods=["*"],		# Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],		# Permite todos os headers
)


# Configurações
UPLOAD_DIR = Path("img/lost")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

UPLOAD_DIR_FOUND = Path("img/found")
UPLOAD_DIR_FOUND.mkdir(parents=True, exist_ok=True)

# Limites e validações
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}


@app.get("/")
async def home():
    return {"mensagem": "Uvicorn rodando com alta performance!"}


def validar_imagem(imagem: UploadFile):
    """Validações da imagem"""
    # Validar extensão
    extensao = Path(imagem.filename).suffix.lower()
    if extensao not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Extensão não permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    # Validar MIME type
    if imagem.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de arquivo não permitido. Use: {', '.join(ALLOWED_MIME_TYPES)}"
        )
    return True


@app.get("/faces")
async def faces() :
    data_atual = datetime.now()
    absolute = "img/lost/" + str(data_atual.year) + f"/{data_atual.month:02d}/"
    try:
        arquivos = listar.listar_arquivos(absolute)
    except:
        print("Caminho invalido")
    id = 0
    result = []
    for arquivo in arquivos:
        if "mb" in arquivo:
            nome = "Michael B. Jordan"
        elif "cm" in arquivo:
            nome = "Cillian Morphy"
        else:
            nome = "r3tnuh"
        result.append(
            {
                "id": id,
                "nome": nome,
                "imageUrl": absolute + arquivo
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
        validar_imagem(imagem)
        # Criar estrutura de pastas por data
        data_atual = datetime.now()
        pasta_data = UPLOAD_DIR_FOUND / str(data_atual.year) / f"{data_atual.month:02d}"
        pasta_data.mkdir(parents=True, exist_ok=True)
        # Gerar nome único
        extensao = Path(imagem.filename).suffix.lower()
        nome = "Unknown"
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
        face =  await face_check.check_face(str(caminho_imagem))
        print(f"saiu da funcao check, resultado:{face}")
        if (not face):
            raise HTTPException(
                    status_code=400,
                    message="Rosto nao detectado"
                )
        print(f"🟢 {nome}, {nome_unico}, {caminho_imagem}, {len(conteudo)}, {imagem.content_type}")
        print("vai retornar")
        return JSONResponse(
            status_code=201,
            content=[{
                "message": "🟢 Pessoa encontrada com sucesso!",
                "id": 42,
                "nome": nome,
                "arquivo": nome_unico,
                "imageUrl": "../controller/img/found/2026/05/20260508_132212_Unknown_6d15db23.jpg",
                "tamanho": len(conteudo),
                "tipo": imagem.content_type,
                "data_upload": datetime.now().isoformat(),
                "similarity": 0.9
            },
            {
                "message": "🟢 Pessoa encontrada com sucesso!",
                "id": 4242,
                "nome": nome,
                "arquivo": nome_unico,
                "imageUrl": "img/found/2026/05/20260508_132212_Unknown_6d15db23.jpg",
                "tamanho": len(conteudo),
                "tipo": imagem.content_type,
                "data_upload": datetime.now().isoformat(),
                "similarity": 0.9
            }
            ]
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
        validar_imagem(imagem)
        # Criar estrutura de pastas por data
        data_atual = datetime.now()
        pasta_data = UPLOAD_DIR / str(data_atual.year) / f"{data_atual.month:02d}"
        pasta_data.mkdir(parents=True, exist_ok=True)
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


# Rota que simula processamento rápido
@app.get("/rapido")
async def rota_rapida():
    hora = datetime.now()
    print(f"TIME:	  {hora.strftime('%Hh%Mm%Ss.%f')}")
    return {"tempo": "Imediato",
            "datetime": hora.strftime('%Hh%Mm%Ss')}


# Rota com I/O simulada
@app.post("/faces/search")
async def io_bound():
    import asyncio
    await asyncio.sleep(0.1)  # Simula consulta banco/API
    return {"processado": "após 100ms"}
