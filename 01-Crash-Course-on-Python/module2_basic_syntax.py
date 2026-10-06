"""
Google IT Automation with Python - Course 1: Crash Course on Python
Module 2: Basic Python Syntax

Covers:
- Functions and return values
- Conditionals (if, elif, else)
- Comparison and logical operators
- Data type conversions (str, int, float)
- Mathematical block storage calculation
"""

from typing import Tuple


def calculate_storage(filesize: int) -> int:
    """
    Calculates storage needed on a filesystem using 4096-byte blocks.
    Mathematical formulation:
      If filesize == 0: returns 4096 (or 0 if empty file consumes no block,
      in filesystem block allocation, any stored file takes ceiling(filesize/block_size)*block_size).
      Coursera specification:
      block_size = 4096
      full_blocks = filesize // block_size
      partial_block_remainder = filesize % block_size
      if partial_block_remainder > 0:
          return (full_blocks + 1) * block_size
      return full_blocks * block_size
    """
    block_size = 4096
    full_blocks = filesize // block_size
    partial_block_remainder = filesize % block_size
    if partial_block_remainder > 0:
        return (full_blocks + 1) * block_size
    return full_blocks * block_size


def color_translator(color: str) -> str:
    """
    Translates color name into hexadecimal representation.
    """
    color_normalized = color.strip().lower()
    if color_normalized == "red":
        return "hex #ff0000"
    elif color_normalized == "green":
        return "hex #00ff00"
    elif color_normalized == "blue":
        return "hex #0000ff"
    else:
        return "unknown"


def exam_grade(score: int) -> str:
    """
    Evaluates student score and returns performance level.
    """
    if score > 95:
        return "Top Score"
    elif score >= 60:
        return "Pass"
    else:
        return "Fail"


def format_name(first_name: str, last_name: str) -> str:
    """
    Formats first and last name into Coursera's required format:
    'Name: last_name, first_name' or single name, or empty string.
    """
    first = first_name.strip()
    last = last_name.strip()
    if first and last:
        return f"Name: {last}, {first}"
    elif first:
        return f"Name: {first}"
    elif last:
        return f"Name: {last}"
    else:
        return ""


def fractional_part(numerator: int, denominator: int) -> float:
    """
    Computes fractional part of numerator / denominator.
    Returns 0.0 if denominator is 0.
    """
    if denominator == 0:
        return 0.0
    return float((numerator % denominator) / denominator)


def convert_distance(miles: float) -> Tuple[float, str]:
    """
    Converts miles to kilometers (1 mile = 1.6 km).
    Returns (km_value, formatted_string).
    """
    km = round(miles * 1.6, 2)
    result_str = f"{miles} miles equals {km} km"
    return km, result_str


def order_numbers(number1: int, number2: int) -> Tuple[int, int]:
    """
    Returns numbers ordered from smallest to largest.
    """
    if number1 > number2:
        return number2, number1
    return number1, number2


def test_module2() -> None:
    """
    Validation assertion test suite for Module 2.
    """
    # 1. calculate_storage
    assert calculate_storage(1) == 4096, "calculate_storage(1) failed"
    assert calculate_storage(4096) == 4096, "calculate_storage(4096) failed"
    assert calculate_storage(4097) == 8192, "calculate_storage(4097) failed"
    assert calculate_storage(6000) == 8192, "calculate_storage(6000) failed"
    assert calculate_storage(0) == 0, "calculate_storage(0) failed"

    # 2. color_translator
    assert color_translator("red") == "hex #ff0000"
    assert color_translator("RED") == "hex #ff0000"
    assert color_translator("green") == "hex #00ff00"
    assert color_translator("blue") == "hex #0000ff"
    assert color_translator("yellow") == "unknown"
    assert color_translator("") == "unknown"

    # 3. exam_grade
    assert exam_grade(100) == "Top Score"
    assert exam_grade(96) == "Top Score"
    assert exam_grade(95) == "Pass"
    assert exam_grade(60) == "Pass"
    assert exam_grade(59) == "Fail"
    assert exam_grade(0) == "Fail"

    # 4. format_name
    assert format_name("Ernest", "Hemingway") == "Name: Hemingway, Ernest"
    assert format_name("", "Madonna") == "Name: Madonna"
    assert format_name("Voltaire", "") == "Name: Voltaire"
    assert format_name("", "") == ""

    # 5. fractional_part
    assert fractional_part(5, 5) == 0.0
    assert fractional_part(5, 4) == 0.25
    assert fractional_part(5, 3) == (5 % 3) / 3
    assert fractional_part(5, 2) == 0.5
    assert fractional_part(5, 0) == 0.0
    assert fractional_part(0, 5) == 0.0

    # 6. convert_distance
    km, msg = convert_distance(55)
    assert km == 88.0
    assert msg == "55 miles equals 88.0 km"

    # 7. order_numbers
    assert order_numbers(100, 99) == (99, 100)
    assert order_numbers(5, 5) == (5, 5)
    assert order_numbers(1, 10) == (1, 10)

    print("[PASS] Module 2: All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module2()
