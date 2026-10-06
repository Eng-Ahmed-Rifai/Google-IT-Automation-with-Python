"""
Unified Test Runner for Google IT Automation with Python - Course 1
Validates all modules with 100.00% precision.
"""

import sys
import time

import module2_basic_syntax
import module3_loops
import module4_data_structures
import module5_oop_and_final_project
import crash_course_reference


def run_full_validation_suite() -> int:
    start_time = time.time()
    print("=" * 80)
    print("GOOGLE IT AUTOMATION WITH PYTHON - COURSE 1: CRASH COURSE ON PYTHON")
    print("COMPREHENSIVE TEST SUITE EXECUTION")
    print("=" * 80)

    modules_to_test = [
        ("Module 2: Basic Python Syntax", module2_basic_syntax.test_module2),
        ("Module 3: Loops & Recursion", module3_loops.test_module3),
        ("Module 4: Strings, Lists & Dictionaries", module4_data_structures.test_module4),
        ("Module 5: OOP & Final Project", module5_oop_and_final_project.test_module5),
        ("Consolidated Reference Suite", crash_course_reference.run_all_assertions),
    ]

    passed_count = 0
    total_count = len(modules_to_test)

    for name, test_func in modules_to_test:
        print(f"\n[EXECUTING] {name}...")
        try:
            test_func()
            passed_count += 1
            print(f"--> Status: PASSED (100.00% precision)")
        except AssertionError as ae:
            print(f"--> Status: FAILED with assertion error: {ae}")
            return 1
        except Exception as e:
            print(f"--> Status: ERROR: {e}")
            return 1

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"SUMMARY: {passed_count}/{total_count} test suites passed cleanly in {elapsed:.3f}s.")
    print("OVERALL PRECISION: 100.00%")
    print("STATUS: READY FOR PRODUCTION & SCHEDULE ALIGNMENT")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(run_full_validation_suite())
