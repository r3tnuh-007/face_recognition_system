# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from utils import listar

app = FastAPI(
    title="API de Alta Performance",
    version="1.0.0"
)

origin = [
    "http://localhost:8000",
    "http://localhost:4242"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],		# Quais sites podem chamar sua API
    allow_credentials=False,	# Permite cookies/auth headers
    allow_methods=["*"],		# Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],		# Permite todos os headers
)

@app.get("/")
async def home():
    return {"mensagem": "Uvicorn rodando com alta performance!"}

@app.get("/faces")
async def faces() :
    absolute = "../controller/img/lost/"
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
@app.get("/io-bound")
async def io_bound():
    import asyncio
    await asyncio.sleep(0.1)  # Simula consulta banco/API
    return {"processado": "após 100ms"}
