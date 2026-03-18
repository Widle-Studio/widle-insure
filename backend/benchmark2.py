import asyncio
import time

import magic

buffer = b"x" * 2048

def sync_task():
    return magic.from_buffer(buffer, mime=True)

async def async_task():
    return await asyncio.to_thread(magic.from_buffer, buffer, mime=True)

async def main():
    n = 1000

    # Simulate 1000 concurrent requests

    start = time.perf_counter()
    for _ in range(n):
        # Even in an async application, calling a sync function will block the event loop
        # so they execute sequentially on the main thread
        sync_task()
    sync_duration = time.perf_counter() - start
    print(f"Sync (Sequential/Blocking) magic x {n}: {sync_duration:.4f}s")

    start = time.perf_counter()
    # In an async application, calling an async function that uses `asyncio.to_thread`
    # will offload the work to thread pool and allow other tasks to run concurrently.
    # To simulate concurrent requests, we use `asyncio.gather`.
    tasks = [async_task() for _ in range(n)]
    await asyncio.gather(*tasks)
    async_duration = time.perf_counter() - start
    print(f"Async (Concurrent/Thread Pool) magic x {n}: {async_duration:.4f}s")

asyncio.run(main())
