# face_recognition_system
Building a face recognion system


# Instalation
```bash
python3 -m venv .venv
source .venv/bin/active.fish
pip install -r requirements.txt
python3 main.py
```

# Extra with mypy
## mypy instalation
```bash
pip install mypy -> but it is already in the requirements.txt
```

## A file verification
```bash
mypy meu_codigo.py
```

## A folder verification
```bash
mypy src/
```

## Ignore libraries without type hint
```bash
mypy --ignore-missing-imports meu_codigo.py
```

### Exemplo de uso do mypy

```python
from typing import Optional

class BancoDeDados:
    def buscar(self, id: int) -> Optional[dict[str, str]]:
        # Pode retornar dict ou None
        return None

def processar_usuario(id: int) -> str:
    db = BancoDeDados()
    usuario = db.buscar(id)

    # Se esquecer de verificar None, mypy avisa!
    return f"Nome: {usuario['nome']}"  # ⚠️ mypy: usuario pode ser None
```
