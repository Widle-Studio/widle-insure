import asyncio
import time
import os
import shutil
import tempfile
from io import BytesIO
import sys

# Add backend to path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from fastapi import UploadFile
from app.services.storage import StorageService

async def simulate_heartbeat():
    """A task that should run every 10ms. We measure how much it gets delayed."""
    max_delay = 0
    delays = []
    # We loop for a while to capture delays during the file uploads.
    for _ in range(500):
        start = time.perf_counter()
        await asyncio.sleep(0.01)
        # Calculate how long the task was delayed beyond the sleep duration.
        delay = (time.perf_counter() - start) - 0.01
        if delay > max_delay:
            max_delay = delay
        delays.append(delay)
    return max_delay, sum(delays)/len(delays)

class DummyFile:
    def __init__(self, size):
        self._file = BytesIO(b"x" * size)

    def read(self, *args, **kwargs):
        return self._file.read(*args, **kwargs)

    @property
    def file(self):
         return self._file

    @property
    def filename(self):
         return "dummy.txt"

async def upload_task(service, file):
    await service.upload_file(file)

async def run_benchmark():
    service = StorageService()

    # Create a 10MB dummy file
    file_size = 10 * 1024 * 1024

    print(f"Starting benchmark: 20 concurrent uploads of {file_size / 1024 / 1024}MB files...")

    start_time = time.perf_counter()

    heartbeat_task = asyncio.create_task(simulate_heartbeat())

    upload_tasks = []
    for i in range(20):
        dummy = DummyFile(file_size)
        file = UploadFile(filename=f"test_{i}.txt", file=dummy.file)
        upload_tasks.append(asyncio.create_task(upload_task(service, file)))

    await asyncio.gather(*upload_tasks)
    max_delay, avg_delay = await heartbeat_task

    total_time = time.perf_counter() - start_time

    print(f"Total time taken: {total_time:.4f} seconds")
    print(f"Maximum event loop blockage (heartbeat delay): {max_delay:.4f} seconds")
    print(f"Average event loop blockage: {avg_delay:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
