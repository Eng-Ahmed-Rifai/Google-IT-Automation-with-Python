"""
Google IT Automation with Python - Course 4: Troubleshooting and Debugging Techniques
Comprehensive Test Suite (test_troubleshooting.py)

Validates all 4 modules using Python's standard unittest framework:
- TestModule1Debugging
- TestModule2PerformanceTuning
- TestModule3CrashResolution
- TestModule4ResourceManagement
"""

import math
import os
import sys
import tempfile
import unittest

# Import all course modules
import module1_debugging as m1
import module2_performance_tuning as m2
import module3_crash_resolution as m3
import module4_resource_management as m4


class TestModule1Debugging(unittest.TestCase):
    """Validation test suite for Module 1: Debugging & Error Isolation"""

    def test_safe_cast_numerics(self):
        self.assertEqual(m1.safe_cast("100", int), 100)
        self.assertEqual(m1.safe_cast("-42", int), -42)
        self.assertEqual(m1.safe_cast("3.14159", float), 3.14159)
        self.assertEqual(m1.safe_cast("15.0", int), 15)

    def test_safe_cast_booleans(self):
        self.assertTrue(m1.safe_cast("True", bool))
        self.assertTrue(m1.safe_cast("yes", bool))
        self.assertTrue(m1.safe_cast("1", bool))
        self.assertFalse(m1.safe_cast("False", bool))
        self.assertFalse(m1.safe_cast("no", bool))
        self.assertFalse(m1.safe_cast("0", bool))

    def test_safe_cast_defaults(self):
        self.assertIsNone(m1.safe_cast("abc", int))
        self.assertEqual(m1.safe_cast("abc", int, default=-1), -1)
        self.assertEqual(m1.safe_cast(None, str, default="empty"), "empty")

    def test_parse_and_validate_record(self):
        schema = {
            "user_id": (int, True, None),
            "username": (str, True, None),
            "quota_mb": (int, False, 1024),
            "is_admin": (bool, False, False)
        }

        # Valid payload
        valid_input = {"user_id": "501", "username": "admin_user", "is_admin": "yes"}
        cleaned, errs = m1.parse_and_validate_record(valid_input, schema)
        self.assertEqual(errs, [])
        self.assertEqual(cleaned["user_id"], 501)
        self.assertEqual(cleaned["username"], "admin_user")
        self.assertEqual(cleaned["quota_mb"], 1024)
        self.assertTrue(cleaned["is_admin"])

        # Missing required field
        missing_input = {"quota_mb": "2048"}
        rec_fail, errs_fail = m1.parse_and_validate_record(missing_input, schema)
        self.assertIsNone(rec_fail)
        self.assertTrue(any("user_id" in e for e in errs_fail))
        self.assertTrue(any("username" in e for e in errs_fail))

    def test_bisect_failing_record(self):
        dataset = [2, 4, 6, 8, "corrupt_data", 10, 12]
        bad_record = m1.bisect_failing_record(dataset, lambda x: isinstance(x, int) and x % 2 == 0)
        self.assertEqual(bad_record, "corrupt_data")

    def test_isolate_log_errors(self):
        log_stream = [
            "2026-10-07 12:00:00 [INFO] Worker started",
            "2026-10-07 12:01:00 [WARNING] CPU usage > 80%",
            "2026-10-07 12:02:00 [ERROR] Failed to connect to replica",
            "2026-10-07 12:03:00 [CRITICAL] Core system panic"
        ]
        isolated = m1.isolate_log_errors(log_stream, ["ERROR", "CRITICAL"])
        self.assertEqual(len(isolated["ERROR"]), 1)
        self.assertIn("Failed to connect", isolated["ERROR"][0])
        self.assertEqual(len(isolated["CRITICAL"]), 1)
        self.assertIn("Core system panic", isolated["CRITICAL"][0])

    def test_isolate_bug_causes(self):
        def test_worker(val):
            if val == "crash":
                raise ValueError("Manual trigger")
            elif val == 0:
                return 10 / val
            return val * 10

        summary = m1.isolate_bug_causes(test_worker, [1, 2, "crash", 0, 4])
        self.assertEqual(summary["success_count"], 3)
        self.assertEqual(summary["failure_count"], 2)
        self.assertEqual(summary["failures_by_exception"]["ValueError"], 1)
        self.assertEqual(summary["failures_by_exception"]["ZeroDivisionError"], 1)


class TestModule2PerformanceTuning(unittest.TestCase):
    """Validation test suite for Module 2: Performance Tuning & Optimization"""

    def test_binary_search_vs_linear_search(self):
        data = list(range(100, 2000, 2))  # 950 sorted elements
        target = 1580

        lin_idx, lin_steps = m2.linear_search(data, target)
        bin_idx, bin_steps = m2.binary_search(data, target)

        self.assertEqual(lin_idx, data.index(target))
        self.assertEqual(bin_idx, data.index(target))
        self.assertEqual(lin_idx, bin_idx)

        # Mathematical logarithmic complexity verification
        max_log_steps = math.ceil(math.log2(len(data))) + 1
        self.assertLessEqual(bin_steps, max_log_steps)
        self.assertGreater(lin_steps, bin_steps * 10)

    def test_binary_search_missing_element(self):
        data = [10, 20, 30, 40, 50]
        idx, _ = m2.binary_search(data, 25)
        self.assertEqual(idx, -1)

    def test_profile_execution(self):
        def sample_task(n):
            return sum(x * 2 for x in range(n))

        prof = m2.profile_execution(sample_task, 50000)
        self.assertEqual(prof["result"], sum(x * 2 for x in range(50000)))
        self.assertGreaterEqual(prof["elapsed_seconds"], 0.0)
        self.assertIn("sample_task", prof["stats_summary"])

    def test_memoize_decorator(self):
        call_count = 0

        @m2.memoize
        def compute_square(x):
            nonlocal call_count
            call_count += 1
            return x * x

        self.assertEqual(compute_square(7), 49)
        self.assertEqual(call_count, 1)

        # Retrieve from cache: call_count must remain 1
        self.assertEqual(compute_square(7), 49)
        self.assertEqual(call_count, 1)

        self.assertEqual(compute_square(8), 64)
        self.assertEqual(call_count, 2)

    def test_run_parallel_batch(self):
        inputs = [100, 200, 300, 400]
        expected = [m2.cpu_heavy_task(x) for x in inputs]
        actual = m2.run_parallel_batch(inputs, max_workers=2)
        self.assertEqual(actual, expected)


class TestModule3CrashResolution(unittest.TestCase):
    """Validation test suite for Module 3: Crash Resolution & Root Cause Investigation"""

    def test_parse_traceback_string(self):
        tb_sample = """
Traceback (most recent call last):
  File "C:/app/service.py", line 105, in handle_request
    data = fetch_record(req_id)
  File "C:/app/db.py", line 55, in fetch_record
    return table[req_id]
KeyError: 'user_999'
        """
        parsed = m3.parse_traceback_string(tb_sample)
        self.assertEqual(parsed["error_type"], "KeyError")
        self.assertEqual(parsed["error_message"], "'user_999'")
        self.assertEqual(len(parsed["frames"]), 2)
        self.assertEqual(parsed["root_cause_frame"]["function"], "fetch_record")
        self.assertEqual(parsed["root_cause_frame"]["line"], 55)

    def test_capture_exception_info(self):
        def error_trigger():
            raise ZeroDivisionError("cannot divide by zero")

        res, err = m3.capture_exception_info(error_trigger)
        self.assertIsNone(res)
        self.assertEqual(err["error_type"], "ZeroDivisionError")
        self.assertIn("cannot divide by zero", err["error_message"])

    def test_memory_leak_tracker(self):
        tracker = m3.MemoryLeakTracker(max_capacity=3)
        tracker.safe_add("k1", "v1")
        tracker.safe_add("k2", "v2")
        tracker.safe_add("k3", "v3")
        self.assertEqual(len(tracker.safe_cache), 3)

        # Adding 4th item triggers eviction of oldest ("k1")
        tracker.safe_add("k4", "v4")
        self.assertEqual(len(tracker.safe_cache), 3)
        self.assertNotIn("k1", tracker.safe_cache)
        self.assertIn("k4", tracker.safe_cache)

        # Check unbounded leaky registry
        for i in range(150):
            tracker.leaky_add(i)
        self.assertTrue(tracker.is_leaking(threshold=100))

    def test_recursion_guard_and_iterative_tree(self):
        # Create deep structure of 60 levels
        deep_node = {"val": 0, "children": []}
        curr = deep_node
        for i in range(1, 60):
            next_node = {"val": i, "children": []}
            curr["children"].append(next_node)
            curr = next_node

        with self.assertRaises(RecursionError):
            m3.guarded_recursive_traversal(deep_node, max_depth=30)

        # Iterative must traverse all 60 nodes without recursion error
        total_counted = m3.iterative_tree_count(deep_node)
        self.assertEqual(total_counted, 60)

    def test_recover_corrupt_json(self):
        valid_raw = '{"status": 200, "message": "OK"}'
        data, ok = m3.recover_corrupt_json(valid_raw)
        self.assertTrue(ok)
        self.assertEqual(data["status"], 200)

        single_quote_raw = "{'status': 500, 'message': 'Internal Error'}"
        data_sq, ok_sq = m3.recover_corrupt_json(single_quote_raw)
        self.assertTrue(ok_sq)
        self.assertEqual(data_sq["status"], 500)

        bad_raw = "{broken_content"
        data_bad, ok_bad = m3.recover_corrupt_json(bad_raw, default_fallback={"fallback": True})
        self.assertFalse(ok_bad)
        self.assertTrue(data_bad["fallback"])


class TestModule4ResourceManagement(unittest.TestCase):
    """Validation test suite for Module 4: Resource Management & Process Lifecycle"""

    def test_atomic_file_write_and_chunked_read(self):
        tmp_dir = tempfile.gettempdir()
        target_path = os.path.join(tmp_dir, "test_resource_atomic.txt")
        content = "System Resource Management Unit Test\n" * 50

        ok = m4.atomic_write_file(target_path, content)
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(target_path))

        chunks = []
        bytes_read = m4.process_file_in_chunks(target_path, chunk_size=64, processor_func=chunks.append)
        self.assertEqual(bytes_read, len(content.encode("utf-8")))
        self.assertGreater(len(chunks), 1)

        if os.path.exists(target_path):
            os.remove(target_path)

    def test_check_disk_threshold(self):
        stat = m4.check_disk_threshold(".", min_free_gb=0.01, min_free_percent=0.1)
        self.assertIn("free_gb", stat)
        self.assertIn("total_gb", stat)
        self.assertTrue(stat["is_healthy"])

    def test_run_process_with_timeout(self):
        # Quick command
        fast_cmd = [sys.executable, "-c", "import sys; sys.stdout.write('proc_ok')"]
        res_fast = m4.run_process_with_timeout(fast_cmd, timeout_seconds=5.0)
        self.assertTrue(res_fast["success"])
        self.assertEqual(res_fast["stdout"], "proc_ok")
        self.assertFalse(res_fast["timed_out"])

        # Timeout command
        slow_cmd = [sys.executable, "-c", "import time; time.sleep(2)"]
        res_slow = m4.run_process_with_timeout(slow_cmd, timeout_seconds=0.3)
        self.assertFalse(res_slow["success"])
        self.assertTrue(res_slow["timed_out"])

    def test_resource_pool_lifecycle(self):
        pool = m4.ResourcePool(capacity=2)
        self.assertEqual(len(pool.available_resources), 2)

        with m4.ManagedResourceContext(pool) as r1:
            self.assertEqual(r1, "res_0")
            self.assertEqual(len(pool.active_resources), 1)
            with m4.ManagedResourceContext(pool) as r2:
                self.assertEqual(r2, "res_1")
                self.assertEqual(len(pool.active_resources), 2)
                # Next acquire must raise RuntimeError
                with self.assertRaises(RuntimeError):
                    pool.acquire()

        # Both resources must be back in pool
        self.assertEqual(len(pool.available_resources), 2)
        self.assertEqual(len(pool.active_resources), 0)


def run_full_suite() -> int:
    """Runs all test cases and returns exit code 0 on complete pass."""
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestModule1Debugging))
    suite.addTests(loader.loadTestsFromTestCase(TestModule2PerformanceTuning))
    suite.addTests(loader.loadTestsFromTestCase(TestModule3CrashResolution))
    suite.addTests(loader.loadTestsFromTestCase(TestModule4ResourceManagement))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_full_suite())
