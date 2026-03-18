import asyncio
import time

import magic

buffer = b"x" * 2048

def sync_task():
    return magic.from_buffer(buffer, mime=True)

async def async_task():
    return await asyncio.to_thread(magic.from_buffer, buffer, mime=True)

async def other_work():
    # simulate IO work
    await asyncio.sleep(0.001)

async def run_sync_with_io(n):
    # simulate event loop blocking
    start = time.perf_counter()
    tasks = []
    for _ in range(n):
        # We spawn a background IO task
        tasks.append(asyncio.create_task(other_work()))

        # But this sync call blocks the event loop from running the background task
        sync_task()

    await asyncio.gather(*tasks)
    return time.perf_counter() - start

async def run_async_with_io(n):
    start = time.perf_counter()
    tasks = []
    magic_tasks = []
    for _ in range(n):
        tasks.append(asyncio.create_task(other_work()))
        magic_tasks.append(asyncio.create_task(async_task()))

    await asyncio.gather(*tasks, *magic_tasks)
    return time.perf_counter() - start

async def main():
    n = 500
    sync_duration = await run_sync_with_io(n)
    print(f"Sync (Blocks Event Loop) magic x {n}: {sync_duration:.4f}s")

    async_duration = await run_async_with_io(n)
    print(f"Async (Thread Pool) magic x {n}: {async_duration:.4f}s")

asyncio.run(main())
