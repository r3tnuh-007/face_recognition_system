import httpx
import asyncio
import time

async def test_performance():
    async with httpx.AsyncClient() as client:
        start = time.time()

        # Faz 100 requisições concorrentes
        tasks = [client.get("http://localhost:8000/rapido") for _ in range(100)]
        responses = await asyncio.gather(*tasks)

        end = time.time()
        total_time = end - start
        requests_per_second = len(responses) / total_time

        print(f"Requisições: {len(responses)}")
        print(f"Tempo total: {total_time:.2f}s")
        print(f"RPS: {requests_per_second:.2f}")

# Rodar
asyncio.run(test_performance())
