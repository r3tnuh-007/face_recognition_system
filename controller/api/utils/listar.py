import os

def listar_arquivos(diretorio: str) -> list[str]:
    """Retorna lista com nomes de todos os arquivos no diretório"""
    try:
        arquivos = [f for f in os.listdir(diretorio)
                   if os.path.isfile(os.path.join(diretorio, f))]
        print(arquivos)
        return arquivos
    except FileNotFoundError:
        print(f"Diretório não encontrado: {diretorio}")
        return []
    except PermissionError:
        print(f"Sem permissão para acessar: {diretorio}")
        return []
