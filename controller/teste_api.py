# main.py
from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI(
    title="API de Alta Performance",
    version="1.0.0"
)

@app.get("/")
async def home():
    return {"mensagem": "Uvicorn rodando com alta performance!"}

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
