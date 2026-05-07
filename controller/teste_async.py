import asyncio

async def tarefa(nome, tempo):
    await asyncio.sleep(tempo)
    return f"{nome} terminou em {tempo}s"

async def main():
    # Criar lista dinâmica de corrotinas
    corrotinas = []

    # Adicionar tasks dinamicamente
    for i in range(10):
        corrotinas.append(tarefa(f"Task_{i}", i * 0.5))


    # Usar * para desempacotar a lista
    resultados = await asyncio.gather(*corrotinas)
    print(resultados)

asyncio.run(main())
