import asyncio
import time

import magic

buffer = b"x" * 2048

def sync_task():
    return magic.from_buffer(buffer, mime=True)

async def async_task():
    return await asyncio.to_thread(magic.from_buffer, buffer, mime=True)

async def simulate_endpoint_sync():
    sync_task()
    await asyncio.sleep(0.01) # fake DB call

async def simulate_endpoint_async():
    await async_task()
    await asyncio.sleep(0.01) # fake DB call

async def main():
    concurrency = 100

    start = time.perf_counter()
    tasks = [simulate_endpoint_sync() for _ in range(concurrency)]
    await asyncio.gather(*tasks)
    sync_duration = time.perf_counter() - start
    print(f"Sync magic - {concurrency} concurrent requests: {sync_duration:.4f}s")

    start = time.perf_counter()
    tasks = [simulate_endpoint_async() for _ in range(concurrency)]
    await asyncio.gather(*tasks)
    async_duration = time.perf_counter() - start
    print(f"Async magic - {concurrency} concurrent requests: {async_duration:.4f}s")

asyncio.run(main())
