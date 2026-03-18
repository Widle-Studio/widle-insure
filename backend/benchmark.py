import asyncio
import time

import magic

buffer = b"x" * 2048

def sync_magic():
    return magic.from_buffer(buffer, mime=True)

async def async_magic():
    return await asyncio.to_thread(magic.from_buffer, buffer, mime=True)

async def main():
    # Warmup
    sync_magic()
    await async_magic()

    n = 1000

    start = time.perf_counter()
    for _ in range(n):
        sync_magic()
    sync_duration = time.perf_counter() - start
    print(f"Sync magic x {n}: {sync_duration:.4f}s")

    start = time.perf_counter()
    for _ in range(n):
        await async_magic()
    async_duration = time.perf_counter() - start
    print(f"Async magic x {n}: {async_duration:.4f}s")

asyncio.run(main())
