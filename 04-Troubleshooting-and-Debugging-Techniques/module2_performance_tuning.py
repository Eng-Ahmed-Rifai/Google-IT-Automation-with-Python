"""
Google IT Automation with Python - Course 4: Troubleshooting and Debugging Techniques
Module 2: Performance Tuning & Optimization (module2_performance_tuning.py)

Covers:
- Profiling tools (cProfile, time execution analysis, bottleneck isolation)
- Concurrency & Multiprocessing (CPU-bound batch processing)
- Algorithmic optimization: O(N) Linear Search vs O(log N) Binary Search
- Caching / Memoization patterns to eliminate redundant computations
"""

import cProfile
import math
import pstats
import io
import time
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Callable, Dict, List, Optional, Tuple


# -------------------------------------------------------------
# 1. ALGORITHMIC OPTIMIZATION: BINARY SEARCH VS LINEAR SEARCH
# -------------------------------------------------------------

def linear_search(items: List[Any], target: Any) -> Tuple[int, int]:
    """
    Performs O(N) linear search.
    Returns: (index_of_target_or_-1, comparisons_count)
    """
    comparisons = 0
    for idx, item in enumerate(items):
        comparisons += 1
        if item == target:
            return idx, comparisons
    return -1, comparisons


def binary_search(sorted_items: List[Any], target: Any) -> Tuple[int, int]:
    """
    Performs O(log N) binary search on a sorted collection.
    Returns: (index_of_target_or_-1, comparisons_count)
    """
    left = 0
    right = len(sorted_items) - 1
    comparisons = 0

    while left <= right:
        comparisons += 1
        mid = (left + right) // 2
        mid_val = sorted_items[mid]

        if mid_val == target:
            return mid, comparisons
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1, comparisons


# -------------------------------------------------------------
# 2. PROFILING & BOTTLENECK IDENTIFICATION
# -------------------------------------------------------------

def profile_execution(func: Callable, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    """
    Profiles the target function using cProfile, capturing runtime metrics and top call statistics.
    Returns a dictionary with execution metrics and string summary.
    """
    profiler = cProfile.Profile()
    start_time = time.perf_counter()
    profiler.enable()

    result = func(*args, **kwargs)

    profiler.disable()
    elapsed_time = time.perf_counter() - start_time

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream).sort_stats("cumulative")
    stats.print_stats(10)

    return {
        "result": result,
        "elapsed_seconds": elapsed_time,
        "total_calls": stats.total_calls,
        "stats_summary": stream.getvalue()
    }


# -------------------------------------------------------------
# 3. CACHING & MEMOIZATION
# -------------------------------------------------------------

def memoize(func: Callable) -> Callable:
    """
    Memoization decorator to cache results for recurring identical arguments.
    """
    cache: Dict[Tuple[Any, ...], Any] = {}

    def wrapper(*args: Any) -> Any:
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    wrapper.cache = cache  # Expose cache for inspection/clearing
    return wrapper


# -------------------------------------------------------------
# 4. MULTIPROCESSING / CONCURRENT BATCH EXECUTION
# -------------------------------------------------------------

def cpu_heavy_task(n: int) -> int:
    """
    Top-level CPU-bound worker function (computes sum of squares)
    Must be defined at module top-level for Windows pickle serialization.
    """
    return sum(i * i for i in range(n))


def run_parallel_batch(
    inputs: List[int],
    max_workers: Optional[int] = 2
) -> List[int]:
    """
    Executes CPU-bound batch tasks across multiple worker processes using ProcessPoolExecutor.
    Falls back gracefully to sequential execution if multiprocessing is restricted.
    """
    if not inputs:
        return []

    try:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(cpu_heavy_task, inputs))
        return results
    except Exception:
        # Fallback to sequential execution
        return [cpu_heavy_task(item) for item in inputs]


# -------------------------------------------------------------
# VALIDATION ASSERTION SUITE
# -------------------------------------------------------------

def test_module2() -> None:
    """
    Strict validation assertion test suite for Module 2.
    """
    # 1. Search Complexity & Correctness
    test_list = list(range(0, 10000, 2))  # 5000 even numbers: 0, 2, 4, ... 9998
    target = 7776  # known element

    idx_lin, comps_lin = linear_search(test_list, target)
    idx_bin, comps_bin = binary_search(test_list, target)

    assert idx_lin == test_list.index(target)
    assert idx_bin == test_list.index(target)
    assert idx_lin == idx_bin

    # Mathematical verification: binary search comparisons must be <= ceil(log2(N)) + 1
    max_expected_comps = math.ceil(math.log2(len(test_list))) + 1
    assert comps_bin <= max_expected_comps, f"Binary search comps {comps_bin} > {max_expected_comps}"
    assert comps_lin > comps_bin * 50, "Binary search must be vastly more efficient than linear search"

    # Missing target check
    idx_missing, _ = binary_search(test_list, 7777)
    assert idx_missing == -1

    # 2. Profiling check
    def sample_workload(count: int) -> int:
        return sum(x for x in range(count))

    prof_data = profile_execution(sample_workload, 100000)
    assert prof_data["result"] == sum(range(100000))
    assert prof_data["elapsed_seconds"] >= 0.0
    assert "sample_workload" in prof_data["stats_summary"]

    # 3. Memoization check
    call_counter = 0

    @memoize
    def slow_multiply(a: int, b: int) -> int:
        nonlocal call_counter
        call_counter += 1
        return a * b

    assert slow_multiply(4, 5) == 20
    assert call_counter == 1
    assert slow_multiply(4, 5) == 20
    assert call_counter == 1  # Result retrieved from cache
    assert slow_multiply(2, 3) == 6
    assert call_counter == 2

    # 4. Multiprocessing / Parallel Batch check
    sample_inputs = [500, 1000, 1500, 2000]
    expected_results = [cpu_heavy_task(x) for x in sample_inputs]
    parallel_results = run_parallel_batch(sample_inputs, max_workers=2)
    assert parallel_results == expected_results

    print("[PASS] Module 2 (Performance Tuning & Optimization): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module2()
