"""
Google IT Automation with Python - Course 4: Troubleshooting and Debugging Techniques
Module 3: Crash Resolution & Root Cause Investigation (module3_crash_resolution.py)

Covers:
- Traceback parsing & root cause isolation (bottom-up call stack analysis)
- Memory leak detection, reference retention, and weakref/eviction patterns
- Runaway recursion mitigation (depth guards & iterative stack transformation)
- Corrupt state & malformed data recovery (safe serialization/deserialization)
"""

import json
import re
import sys
import traceback
import weakref
from typing import Any, Callable, Dict, List, Optional, Tuple


# -------------------------------------------------------------
# 1. TRACEBACK PARSING & STACK INVESTIGATION
# -------------------------------------------------------------

def parse_traceback_string(tb_text: str) -> Dict[str, Any]:
    """
    Parses a standard Python traceback string from bottom to top.
    Extracts:
      - error_type: Exception class name
      - error_message: Human-readable error message
      - frames: List of dicts representing the call stack
      - root_cause_frame: The deepest application frame where the exception occurred
    """
    lines = [line.rstrip() for line in tb_text.strip().splitlines() if line.strip()]
    if not lines:
        return {"error_type": "Unknown", "error_message": "", "frames": [], "root_cause_frame": None}

    # Extract exception type and message from the final line
    last_line = lines[-1]
    if ":" in last_line:
        error_type, error_message = last_line.split(":", 1)
        error_type = error_type.strip()
        error_message = error_message.strip()
    else:
        error_type = last_line.strip()
        error_message = ""

    # Parse stack frames (File "...", line ..., in ...)
    frame_pattern = re.compile(r'File\s+"([^"]+)",\s+line\s+(\d+),\s+in\s+(\w+)')
    frames: List[Dict[str, Any]] = []

    for i, line in enumerate(lines[:-1]):
        match = frame_pattern.search(line)
        if match:
            filepath, lineno, func_name = match.groups()
            code_snippet = ""
            if i + 1 < len(lines[:-1]) and not frame_pattern.search(lines[i + 1]):
                code_snippet = lines[i + 1].strip()
            frames.append({
                "file": filepath,
                "line": int(lineno),
                "function": func_name,
                "code": code_snippet
            })

    root_cause_frame = frames[-1] if frames else None

    return {
        "error_type": error_type,
        "error_message": error_message,
        "frames": frames,
        "root_cause_frame": root_cause_frame
    }


def capture_exception_info(func: Callable, *args: Any, **kwargs: Any) -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    """
    Executes func safely. If an exception occurs, captures full traceback information.
    Returns (result, None) on success or (None, parsed_traceback_dict) on exception.
    """
    try:
        res = func(*args, **kwargs)
        return res, None
    except Exception:
        tb_str = traceback.format_exc()
        parsed = parse_traceback_string(tb_str)
        return None, parsed


# -------------------------------------------------------------
# 2. MEMORY LEAK SIMULATION & LEAK PREVENTION
# -------------------------------------------------------------

class MemoryLeakTracker:
    """
    Simulates and detects memory leaks caused by unbounded reference retention.
    Demonstrates both leaky retention and bounded weakref/LRU eviction.
    """
    def __init__(self, max_capacity: int = 100) -> None:
        self.max_capacity = max_capacity
        self.leaky_registry: List[Any] = []
        self.safe_cache: Dict[str, Any] = {}
        self.access_history: List[str] = []

    def leaky_add(self, item: Any) -> None:
        """Simulates a leak: continually appends items to an unbounded list."""
        self.leaky_registry.append(item)

    def safe_add(self, key: str, value: Any) -> None:
        """Prevents memory leak: maintains bounded capacity via FIFO eviction."""
        if len(self.safe_cache) >= self.max_capacity and key not in self.safe_cache:
            evict_key = self.access_history.pop(0)
            self.safe_cache.pop(evict_key, None)

        self.safe_cache[key] = value
        if key in self.access_history:
            self.access_history.remove(key)
        self.access_history.append(key)

    def is_leaking(self, threshold: int = 200) -> bool:
        """Detects if unbounded registry exceeds safety threshold."""
        return len(self.leaky_registry) > threshold


# -------------------------------------------------------------
# 3. RUNAWAY RECURSION MITIGATION (DEPTH GUARDS)
# -------------------------------------------------------------

def guarded_recursive_traversal(
    node: Dict[str, Any],
    max_depth: int = 50,
    current_depth: int = 0
) -> int:
    """
    Safely traverses recursive trees/graphs with a recursion depth guard.
    Prevents RecursionError when encountering cyclic or excessively deep structures.
    """
    if current_depth > max_depth:
        raise RecursionError(f"Recursion guard triggered: exceeded max depth {max_depth}")

    count = 1
    for child in node.get("children", []):
        count += guarded_recursive_traversal(child, max_depth, current_depth + 1)
    return count


def iterative_tree_count(root: Dict[str, Any]) -> int:
    """
    Converts deep recursive tree traversal into an iterative stack implementation.
    Immune to call-stack recursion limits.
    """
    stack = [root]
    count = 0
    while stack:
        current = stack.pop()
        count += 1
        for child in current.get("children", []):
            stack.append(child)
    return count


# -------------------------------------------------------------
# 4. CORRUPT STATE RECOVERY
# -------------------------------------------------------------

def recover_corrupt_json(
    raw_payload: str,
    default_fallback: Optional[Dict[str, Any]] = None
) -> Tuple[Dict[str, Any], bool]:
    """
    Attempts to parse JSON data. If corrupted or malformed, isolates the failure
    and returns a clean fallback dictionary with a recovered flag.
    Returns: (parsed_data, is_recovered_or_valid)
    """
    if default_fallback is None:
        default_fallback = {}

    try:
        data = json.loads(raw_payload)
        return data, True
    except (json.JSONDecodeError, TypeError):
        # Attempt basic sanitation: check if single quotes were used instead of double quotes
        try:
            sanitized = raw_payload.replace("'", '"')
            data = json.loads(sanitized)
            return data, True
        except Exception:
            return default_fallback, False


# -------------------------------------------------------------
# VALIDATION ASSERTION SUITE
# -------------------------------------------------------------

def test_module3() -> None:
    """
    Strict validation assertion test suite for Module 3.
    """
    # 1. Traceback parsing test
    sample_traceback = """
Traceback (most recent call last):
  File "C:/app/main.py", line 42, in process_data
    result = compute(item)
  File "C:/app/math_ops.py", line 18, in compute
    return 100 / value
ZeroDivisionError: division by zero
    """
    parsed = parse_traceback_string(sample_traceback)
    assert parsed["error_type"] == "ZeroDivisionError"
    assert parsed["error_message"] == "division by zero"
    assert len(parsed["frames"]) == 2
    assert parsed["root_cause_frame"]["function"] == "compute"
    assert parsed["root_cause_frame"]["line"] == 18

    # 2. Exception capture test
    def fail_func():
        raise KeyError("missing_config_key")

    res, err = capture_exception_info(fail_func)
    assert res is None
    assert err["error_type"] == "KeyError"
    assert "missing_config_key" in err["error_message"]

    # 3. Memory leak tracker test
    tracker = MemoryLeakTracker(max_capacity=5)
    for i in range(10):
        tracker.safe_add(f"key_{i}", f"val_{i}")
    assert len(tracker.safe_cache) == 5, "Safe cache failed to maintain bounded capacity"
    assert "key_9" in tracker.safe_cache
    assert "key_0" not in tracker.safe_cache  # Evicted

    for i in range(250):
        tracker.leaky_add(i)
    assert tracker.is_leaking(threshold=200) is True

    # 4. Recursion guard test
    # Create a deep linear chain of 70 nodes
    deep_tree = {"val": 0, "children": []}
    curr = deep_tree
    for i in range(1, 70):
        new_node = {"val": i, "children": []}
        curr["children"].append(new_node)
        curr = new_node

    # Guard should trigger at depth 50
    recursion_caught = False
    try:
        guarded_recursive_traversal(deep_tree, max_depth=50)
    except RecursionError:
        recursion_caught = True
    assert recursion_caught is True

    # Iterative traversal should succeed completely
    total_nodes = iterative_tree_count(deep_tree)
    assert total_nodes == 70

    # 5. Corrupt JSON recovery test
    valid_json = '{"user": "ahmed", "status": "active"}'
    data_valid, ok_valid = recover_corrupt_json(valid_json)
    assert ok_valid is True
    assert data_valid["user"] == "ahmed"

    single_quoted_json = "{'user': 'rifai', 'status': 'ok'}"
    data_sq, ok_sq = recover_corrupt_json(single_quoted_json)
    assert ok_sq is True
    assert data_sq["user"] == "rifai"

    irrecoverable = "{broken json payload"
    data_irrec, ok_irrec = recover_corrupt_json(irrecoverable, default_fallback={"error": True})
    assert ok_irrec is False
    assert data_irrec == {"error": True}

    print("[PASS] Module 3 (Crash Resolution & Root Cause Investigation): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module3()
