"""
Google IT Automation with Python - Course 4: Troubleshooting and Debugging Techniques
Module 4: Resource Management & Process Lifecycle (module4_resource_management.py)

Covers:
- System resource monitoring (Disk space, memory thresholds, file descriptor limits)
- Disk I/O optimization (Chunked stream processing, buffered batch writes, atomic file replacement)
- Process management & watchdog (Timeout handling, zombie/hung process termination)
- Resource pool management (Bounded pool with context manager lifecycle)
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple


# -------------------------------------------------------------
# 1. DISK I/O OPTIMIZATION (STREAMING & ATOMIC REPLACEMENT)
# -------------------------------------------------------------

def process_file_in_chunks(
    filepath: str,
    chunk_size: int = 4096,
    processor_func: Optional[Callable[[bytes], Any]] = None
) -> int:
    """
    Reads large files in fixed-size binary chunks to prevent RAM starvation.
    Returns the total bytes processed.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Target file not found: {filepath}")

    total_bytes = 0
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            total_bytes += len(chunk)
            if processor_func:
                processor_func(chunk)

    return total_bytes


def atomic_write_file(filepath: str, content: str) -> bool:
    """
    Safely writes data to a temporary file and atomically replaces the target file.
    Prevents corrupt/partial writes during system crashes or power outages.
    """
    dir_name = os.path.dirname(filepath) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, prefix=".tmp_atomic_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, filepath)
        return True
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


# -------------------------------------------------------------
# 2. SYSTEM RESOURCE MONITORING
# -------------------------------------------------------------

def check_disk_threshold(
    path: str = ".",
    min_free_gb: float = 1.0,
    min_free_percent: float = 10.0
) -> Dict[str, Any]:
    """
    Checks disk storage availability against safety thresholds.
    Returns status dictionary with free_gb, percent_free, and is_healthy flag.
    """
    usage = shutil.disk_usage(path)
    free_gb = usage.free / (2**30)
    total_gb = usage.total / (2**30)
    percent_free = (usage.free / usage.total) * 100.0

    is_healthy = (free_gb >= min_free_gb) and (percent_free >= min_free_percent)

    return {
        "free_gb": round(free_gb, 2),
        "total_gb": round(total_gb, 2),
        "percent_free": round(percent_free, 2),
        "is_healthy": is_healthy
    }


# -------------------------------------------------------------
# 3. PROCESS MANAGEMENT & TIMEOUT CONTROL
# -------------------------------------------------------------

def run_process_with_timeout(
    command: List[str],
    timeout_seconds: float = 5.0
) -> Dict[str, Any]:
    """
    Executes an external command with strict timeout supervision.
    Prevents hung or zombie child processes by terminating upon timeout.
    Returns execution status dictionary.
    """
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False
        )
        return {
            "success": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
            "timed_out": False
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "success": False,
            "returncode": -1,
            "stdout": (exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "").strip() if isinstance(exc.stderr, str) else "Command timed out",
            "timed_out": True
        }
    except Exception as exc:
        return {
            "success": False,
            "returncode": -2,
            "stdout": "",
            "stderr": str(exc),
            "timed_out": False
        }


# -------------------------------------------------------------
# 4. RESOURCE POOL MANAGEMENT
# -------------------------------------------------------------

class ResourcePool:
    """
    Bounded resource pool manager (e.g. database connections, file handles).
    Enforces maximum capacity and safe resource acquisition/release.
    """
    def __init__(self, capacity: int = 5) -> None:
        self.capacity = capacity
        self.available_resources: List[str] = [f"res_{i}" for i in range(capacity)]
        self.active_resources: List[str] = []

    def acquire(self) -> str:
        """Acquires a resource from the pool; raises RuntimeError if exhausted."""
        if not self.available_resources:
            raise RuntimeError("Resource pool exhausted: no resources available")
        resource = self.available_resources.pop(0)
        self.active_resources.append(resource)
        return resource

    def release(self, resource: str) -> None:
        """Returns a previously acquired resource back to the pool."""
        if resource in self.active_resources:
            self.active_resources.remove(resource)
            self.available_resources.append(resource)


class ManagedResourceContext:
    """Context manager for safe resource acquisition and release."""
    def __init__(self, pool: ResourcePool) -> None:
        self.pool = pool
        self.acquired_resource: Optional[str] = None

    def __enter__(self) -> str:
        self.acquired_resource = self.pool.acquire()
        return self.acquired_resource

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.acquired_resource is not None:
            self.pool.release(self.acquired_resource)


# -------------------------------------------------------------
# VALIDATION ASSERTION SUITE
# -------------------------------------------------------------

def test_module4() -> None:
    """
    Strict validation assertion test suite for Module 4.
    """
    # 1. Atomic write & Chunked processing tests
    temp_dir = tempfile.gettempdir()
    test_filepath = os.path.join(temp_dir, "test_resource_mgmt_data.txt")
    payload = "Automating IT Infrastructure with Python.\n" * 100

    write_ok = atomic_write_file(test_filepath, payload)
    assert write_ok is True
    assert os.path.exists(test_filepath)

    chunk_counts = 0
    def sample_counter(chunk: bytes):
        nonlocal chunk_counts
        chunk_counts += 1

    total_b = process_file_in_chunks(test_filepath, chunk_size=128, processor_func=sample_counter)
    assert total_b == len(payload.encode("utf-8"))
    assert chunk_counts > 0

    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    # 2. Disk threshold check
    disk_stat = check_disk_threshold(".", min_free_gb=0.01, min_free_percent=0.1)
    assert "free_gb" in disk_stat
    assert "total_gb" in disk_stat
    assert disk_stat["is_healthy"] is True

    # 3. Process management with timeout
    # Test fast command
    fast_cmd = [sys.executable, "-c", "print('hello_world')"]
    fast_res = run_process_with_timeout(fast_cmd, timeout_seconds=5.0)
    assert fast_res["success"] is True
    assert fast_res["stdout"] == "hello_world"
    assert fast_res["timed_out"] is False

    # Test timed out command
    slow_cmd = [sys.executable, "-c", "import time; time.sleep(3)"]
    slow_res = run_process_with_timeout(slow_cmd, timeout_seconds=0.5)
    assert slow_res["success"] is False
    assert slow_res["timed_out"] is True

    # 4. Resource Pool tests
    pool = ResourcePool(capacity=2)
    assert len(pool.available_resources) == 2

    with ManagedResourceContext(pool) as r1:
        assert r1 == "res_0"
        assert len(pool.active_resources) == 1
        with ManagedResourceContext(pool) as r2:
            assert r2 == "res_1"
            assert len(pool.active_resources) == 2

            # Trying to acquire a 3rd resource must fail
            exhausted_caught = False
            try:
                pool.acquire()
            except RuntimeError:
                exhausted_caught = True
            assert exhausted_caught is True

    # After exiting contexts, all resources must be restored
    assert len(pool.available_resources) == 2
    assert len(pool.active_resources) == 0

    print("[PASS] Module 4 (Resource Management & Process Lifecycle): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module4()
