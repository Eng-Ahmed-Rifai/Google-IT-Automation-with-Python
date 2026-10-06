"""
Google IT Automation with Python - Course 1: Crash Course on Python
Module 3: Loops & Recursion

Covers:
- While loops & loop termination
- For loops & range(start, stop, step)
- Nested loops (e.g. Domino tiles, multiplication tables)
- Loop control: break and continue
- Recursion: base cases, recursive transitions, call stack integrity
"""

from typing import List, Tuple


def is_power_of_two(number: int) -> bool:
    """
    Checks if number is a power of 2 using a while loop.
    A positive integer n is a power of two if dividing by 2 repeatedly reaches 1.
    """
    if number <= 0:
        return False
    while number % 2 == 0:
        number = number // 2
    return number == 1


def sum_divisors(n: int) -> int:
    """
    Returns the sum of all proper divisors of n (from 1 up to n-1).
    Special cases:
      n <= 1 returns 0.
      e.g. 6 -> 1 + 2 + 3 = 6
      e.g. 12 -> 1 + 2 + 3 + 4 + 6 = 16
    """
    if n <= 1:
        return 0
    total = 0
    divisor = 1
    while divisor < n:
        if n % divisor == 0:
            total += divisor
        divisor += 1
    return total


def multiplication_table(start: int, stop: int) -> List[str]:
    """
    Generates multiplication table entries from start to stop inclusive.
    Utilizes nested for loops.
    """
    results: List[str] = []
    for x in range(start, stop + 1):
        for y in range(start, stop + 1):
            results.append(f"{x}x{y}={x * y}")
    return results


def counter(start: int, stop: int) -> str:
    """
    Counts from start to stop in steps of 1 (either ascending or descending),
    returning space-separated numbers as string.
    """
    if start <= stop:
        numbers = [str(x) for x in range(start, stop + 1)]
    else:
        numbers = [str(x) for x in range(start, stop - 1, -1)]
    return " ".join(numbers)


def count_digits(n: int) -> int:
    """
    Counts number of digits in an integer n using while loop.
    Handles negative numbers and 0 correctly.
    """
    n = abs(n)
    if n == 0:
        return 1
    count = 0
    while n > 0:
        count += 1
        n = n // 10
    return count


def factorial_iterative(n: int) -> int:
    """
    Computes n! iteratively with input validation.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int:
    """
    Computes n! recursively. Base case: n <= 1 -> 1.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def sum_positive_numbers(n: int) -> int:
    """
    Recursively sums all positive integers from 1 up to n.
    Base case: n <= 1.
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return n + sum_positive_numbers(n - 1)


def is_power_of(number: int, base: int) -> bool:
    """
    Recursively or iteratively checks if number is power of base.
    base must be > 1. number must be >= 1.
    """
    if number <= 0 or base <= 1:
        return False
    if number == 1:
        return True
    if number % base != 0:
        return False
    return is_power_of(number // base, base)


def domino_tiles() -> List[Tuple[int, int]]:
    """
    Generates standard set of domino tiles (0 to 6) without duplicates.
    Total should be (7 * 8) / 2 = 28 tiles.
    """
    tiles: List[Tuple[int, int]] = []
    for left in range(7):
        for right in range(left, 7):
            tiles.append((left, right))
    return tiles


def even_numbers_filter(maximum: int) -> List[int]:
    """
    Demonstrates continue and break in a loop:
    Collects even numbers up to maximum. Stops early if exceeding 100.
    """
    evens: List[int] = []
    for num in range(maximum + 1):
        if num > 100:
            break
        if num % 2 != 0:
            continue
        evens.append(num)
    return evens


def test_module3() -> None:
    """
    Validation assertion test suite for Module 3.
    """
    # 1. is_power_of_two
    assert is_power_of_two(0) is False
    assert is_power_of_two(1) is True
    assert is_power_of_two(2) is True
    assert is_power_of_two(8) is True
    assert is_power_of_two(9) is False
    assert is_power_of_two(-8) is False
    assert is_power_of_two(1024) is True

    # 2. sum_divisors
    assert sum_divisors(0) == 0
    assert sum_divisors(1) == 0  # proper divisor does not include 1
    assert sum_divisors(6) == 1 + 2 + 3  # 6
    assert sum_divisors(12) == 1 + 2 + 3 + 4 + 6  # 16
    assert sum_divisors(36) == 1 + 2 + 3 + 4 + 6 + 9 + 12 + 18  # 55

    # 3. multiplication_table
    table = multiplication_table(1, 3)
    assert len(table) == 9
    assert table[0] == "1x1=1"
    assert table[-1] == "3x3=9"

    # 4. counter
    assert counter(1, 4) == "1 2 3 4"
    assert counter(4, 1) == "4 3 2 1"
    assert counter(2, 2) == "2"

    # 5. count_digits
    assert count_digits(0) == 1
    assert count_digits(7) == 1
    assert count_digits(25) == 2
    assert count_digits(1000) == 4
    assert count_digits(-999) == 3

    # 6. factorials
    for i in range(10):
        assert factorial_iterative(i) == factorial_recursive(i)
    assert factorial_recursive(5) == 120
    assert factorial_iterative(0) == 1

    # 7. sum_positive_numbers
    assert sum_positive_numbers(0) == 0
    assert sum_positive_numbers(3) == 6
    assert sum_positive_numbers(5) == 15
    assert sum_positive_numbers(10) == 55

    # 8. is_power_of
    assert is_power_of(8, 2) is True
    assert is_power_of(64, 4) is True
    assert is_power_of(70, 10) is False
    assert is_power_of(1, 5) is True
    assert is_power_of(0, 2) is False

    # 9. domino_tiles
    dominoes = domino_tiles()
    assert len(dominoes) == 28
    assert dominoes[0] == (0, 0)
    assert dominoes[-1] == (6, 6)

    # 10. even_numbers_filter
    evens = even_numbers_filter(10)
    assert evens == [0, 2, 4, 6, 8, 10]
    evens_large = even_numbers_filter(150)
    assert evens_large[-1] == 100

    print("[PASS] Module 3: All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module3()
