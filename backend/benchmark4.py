import asyncio
import time

import magic

buffer = b"x" * 2048

def sync_task():
    return magic.from_buffer(buffer, mime=True)

async def async_task():
    return await asyncio.to_thread(magic.from_buffer, buffer, mime=True)

async def worker_sync(n):
    for _ in range(n):
        sync_task()
        await asyncio.sleep(0) # yield control

async def worker_async(n):
    for _ in range(n):
        await async_task()

async def simulate_slow_io():
    start = time.perf_counter()
    await asyncio.sleep(0.5)
    return time.perf_counter() - start

async def main():
    n = 1000

    # 1. Test event loop starvation with sync_task
    print("Test 1: Sync task blocking the event loop")
    start = time.perf_counter()
    # We start a fast background task
    io_task = asyncio.create_task(simulate_slow_io())

    # And we run a bunch of sync tasks that block the loop
    await worker_sync(n)

    io_time = await io_task
    total_time = time.perf_counter() - start
    print(f"Total time: {total_time:.4f}s")
    print(f"Time for 0.5s IO task to complete: {io_time:.4f}s (should be ~0.5s)")

    print("-" * 40)

    # 2. Test event loop with async_task
    print("Test 2: Async task non-blocking the event loop")
    start = time.perf_counter()
    # We start a fast background task
    io_task = asyncio.create_task(simulate_slow_io())

    # And we run a bunch of async tasks that offload to thread pool
    await worker_async(n)

    io_time = await io_task
    total_time = time.perf_counter() - start
    print(f"Total time: {total_time:.4f}s")
    print(f"Time for 0.5s IO task to complete: {io_time:.4f}s (should be ~0.5s)")

asyncio.run(main())
