"""
Google IT Automation with Python - Course 4: Troubleshooting and Debugging Techniques
Module 1: Debugging & Error Isolation (module1_debugging.py)

Covers:
- Systematic debugging methodology: Reproduce -> Isolate -> Root Cause -> Fix & Verify
- Robust type conversions and safe casting with fallback defaults
- Error isolation via bisecting / delta debugging on malformed datasets
- Log parsing and anomaly isolation
- Schema-based record validation and data sanitization
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

# Configure module-level logger for debugging trace
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("debugging_module")


def safe_cast(
    val: Any,
    target_type: Type,
    default: Any = None
) -> Any:
    """
    Safely converts a value to target_type (int, float, bool, str) without unhandled exceptions.
    Handles string booleans ('true', 'false', '1', '0') and numeric strings cleanly.
    """
    if val is None:
        return default

    try:
        if target_type is bool:
            if isinstance(val, str):
                cleaned = val.strip().lower()
                if cleaned in ("true", "1", "yes", "t", "y"):
                    return True
                elif cleaned in ("false", "0", "no", "f", "n", ""):
                    return False
                return default
            return bool(val)

        if target_type in (int, float):
            if isinstance(val, str):
                cleaned = val.strip()
                if not cleaned:
                    return default
                # Allow int casting from float strings (e.g., "12.0" -> 12)
                if target_type is int:
                    return int(float(cleaned))
                return float(cleaned)
            return target_type(val)

        if target_type is str:
            return str(val)

        return target_type(val)
    except (ValueError, TypeError, OverflowError):
        return default


def parse_and_validate_record(
    raw_data: Dict[str, Any],
    schema: Dict[str, Tuple[Type, bool, Any]]
) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    """
    Validates and casts a raw record against a schema definition.
    Schema format: {field_name: (target_type, is_required, default_value)}
    Returns: (cleaned_record_or_None, list_of_error_messages)
    """
    errors: List[str] = []
    cleaned: Dict[str, Any] = {}

    for field, (expected_type, required, default_val) in schema.items():
        if field not in raw_data or raw_data[field] is None or raw_data[field] == "":
            if required:
                errors.append(f"Missing required field: '{field}'")
            else:
                cleaned[field] = default_val
            continue

        converted = safe_cast(raw_data[field], expected_type, default=None)
        if converted is None:
            if required:
                errors.append(
                    f"Field '{field}' with value '{raw_data[field]}' could not be cast to {expected_type.__name__}"
                )
            else:
                cleaned[field] = default_val
        else:
            cleaned[field] = converted

    if errors:
        return None, errors
    return cleaned, []


def bisect_failing_record(
    records: List[Any],
    predicate: Callable[[Any], bool]
) -> Optional[Any]:
    """
    Linear/Binary search debugging pattern (Delta debugging / Git bisect):
    Identifies the first failing record in a list where predicate(record) raises an exception or returns False.
    """
    for index, record in enumerate(records):
        try:
            passed = predicate(record)
            if not passed:
                return record
        except Exception:
            return record
    return None


def isolate_log_errors(
    log_lines: List[str],
    severity_levels: Optional[List[str]] = None
) -> Dict[str, List[str]]:
    """
    Parses raw log streams, isolating errors by severity level and extracting clean messages.
    Default severities: ['ERROR', 'CRITICAL'].
    """
    if severity_levels is None:
        severity_levels = ["ERROR", "CRITICAL"]

    normalized_levels = [lvl.upper() for lvl in severity_levels]
    isolated: Dict[str, List[str]] = {lvl: [] for lvl in normalized_levels}

    for line in log_lines:
        line_clean = line.strip()
        for lvl in normalized_levels:
            token = f"[{lvl}]"
            alt_token = f"{lvl}:"
            if token in line_clean or alt_token in line_clean or f" {lvl} " in line_clean:
                isolated[lvl].append(line_clean)
                break

    return isolated


def isolate_bug_causes(
    target_func: Callable[[Any], Any],
    inputs: List[Any]
) -> Dict[str, Any]:
    """
    Executes target_func against a batch of test inputs, separating successes from failures
    and grouping failures by exception type.
    """
    results: Dict[str, Any] = {
        "success_count": 0,
        "failure_count": 0,
        "failures_by_exception": {},
        "problematic_inputs": []
    }

    for item in inputs:
        try:
            _ = target_func(item)
            results["success_count"] += 1
        except Exception as ex:
            results["failure_count"] += 1
            ex_name = type(ex).__name__
            results["failures_by_exception"][ex_name] = (
                results["failures_by_exception"].get(ex_name, 0) + 1
            )
            results["problematic_inputs"].append({
                "input": item,
                "error_type": ex_name,
                "error_message": str(ex)
            })

    return results


def test_module1() -> None:
    """
    Strict validation assertion test suite for Module 1.
    """
    # 1. safe_cast tests
    assert safe_cast("42", int) == 42
    assert safe_cast("3.14159", float) == 3.14159
    assert safe_cast("invalid", int, default=0) == 0
    assert safe_cast("True", bool) is True
    assert safe_cast("no", bool) is False
    assert safe_cast(None, str, default="N/A") == "N/A"
    assert safe_cast("100.5", int) == 100

    # 2. Schema validation tests
    schema = {
        "id": (int, True, None),
        "username": (str, True, None),
        "score": (float, False, 0.0),
        "is_active": (bool, False, True),
    }

    valid_record = {"id": "101", "username": "ahmed", "score": "98.5", "is_active": "yes"}
    rec, errs = parse_and_validate_record(valid_record, schema)
    assert errs == []
    assert rec == {"id": 101, "username": "ahmed", "score": 98.5, "is_active": True}

    invalid_record = {"id": "bad_id", "username": "ahmed"}
    rec_bad, errs_bad = parse_and_validate_record(invalid_record, schema)
    assert rec_bad is None
    assert any("bad_id" in e for e in errs_bad)

    # 3. Bisect / Delta debugging test
    data_stream = [10, 20, 30, "corrupted", 50, 60]
    bad_item = bisect_failing_record(data_stream, lambda x: isinstance(x, int) and x > 0)
    assert bad_item == "corrupted"

    # 4. Log isolation tests
    logs = [
        "2026-10-07 10:00:00 [INFO] System initialized",
        "2026-10-07 10:01:00 [ERROR] Connection timed out to db",
        "2026-10-07 10:02:00 [CRITICAL] Out of memory condition detected",
        "2026-10-07 10:03:00 [WARNING] Disk space above 80%",
    ]
    isolated = isolate_log_errors(logs)
    assert len(isolated["ERROR"]) == 1
    assert "Connection timed out" in isolated["ERROR"][0]
    assert len(isolated["CRITICAL"]) == 1
    assert "Out of memory" in isolated["CRITICAL"][0]

    # 5. Bug cause isolation test
    def fragile_function(x):
        if x == "crash":
            raise ValueError("Intentional crash")
        if x == 0:
            return 100 / x
        return x * 2

    inputs = [1, 2, "crash", 0, 5]
    diag = isolate_bug_causes(fragile_function, inputs)
    assert diag["success_count"] == 3
    assert diag["failure_count"] == 2
    assert diag["failures_by_exception"]["ValueError"] == 1
    assert diag["failures_by_exception"]["ZeroDivisionError"] == 1

    print("[PASS] Module 1 (Debugging & Error Isolation): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module1()
