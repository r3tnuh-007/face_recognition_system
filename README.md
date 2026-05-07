# face_recognition_system
## Project Info
```markdown
**Nome:** _FindMyPerson_

**Description:** _Uma plataforma que ajuda os usuários a localizarem alguém perdido por meio de reconhecimento facial. Se alguém desapareceu, na vida real, o usuário vai na plataforma e publica uma foto da pessoa desaparecida e as suas informações de contacto. Se alguém encontrar alguém perdido que por algum motivo não consiga se comunicar, ou os responsáveis por essa pessoa não aparecem basta tirar uma foto da pessoa e colocar ela na categoria de encontrada, o sistema por meio de reconhecimento facial fará o match do rosto, caso o rosto perdido esteja na base de dados de rostos encontrados notifica os usuários._
```

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

# Emojis que serão usados ao longo do projeto

``` bash
🫥☠️👾🥶🥵🌍🌕💤🚫⛔⁉️‼️♊🇦🇴🟢⚠️❌
```
