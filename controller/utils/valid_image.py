from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status, Request
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path


# Limites e validações
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}

def validar_imagem(imagem: UploadFile) -> bool:
    """Validações da imagem"""
    # Validar extensão
    extensao = Path(imagem.filename).suffix.lower()
    if extensao not in ALLOWED_EXTENSIONS:
        return False
    # Validar MIME type
    if imagem.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de arquivo não permitido. Use: {', '.join(ALLOWED_MIME_TYPES)}"
        )
    return True
