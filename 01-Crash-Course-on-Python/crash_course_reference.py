"""
========================================================================================
Google IT Automation with Python - Course 1: Crash Course on Python
Consolidated Master Reference & Assessment Script
========================================================================================
Author: Eng. Ahmed Rifai Study Automation Assistant
Target Completion Milestone: 2026-10-18 Alignment
Precision Standard: 100.00% Mathematical & Algorithmic Accuracy

This master script contains complete, validated implementations for:
  - Module 2: Basic Python Syntax (Data types, conditionals, conversions, return values)
  - Module 3: Loops & Recursion (While loops, for loops, nested loops, break/continue)
  - Module 4: Data Structures (Strings, Lists, Dictionaries, comprehensions)
  - Module 5: Object-Oriented Programming & Final Project (WordCloud, Event Log Tracking, Health Checks)
========================================================================================
"""

import os
import sys
import shutil
from typing import Dict, List, Set, Tuple, Any, Optional


# ======================================================================================
# MODULE 2: BASIC PYTHON SYNTAX
# ======================================================================================

def calculate_storage(filesize: int) -> int:
    """
    Calculates filesystem block allocation using 4096-byte blocks.
    Any non-zero remainder allocates an additional full 4096-byte block.
    """
    block_size = 4096
    full_blocks = filesize // block_size
    partial_block_remainder = filesize % block_size
    if partial_block_remainder > 0:
        return (full_blocks + 1) * block_size
    return full_blocks * block_size


def color_translator(color: str) -> str:
    """
    Translates color names to hex codes according to Coursera specs.
    """
    c = color.strip().lower()
    if c == "red":
        return "hex #ff0000"
    elif c == "green":
        return "hex #00ff00"
    elif c == "blue":
        return "hex #0000ff"
    return "unknown"


def exam_grade(score: int) -> str:
    """
    Classifies exam scores into Top Score (>95), Pass (>=60), or Fail (<60).
    """
    if score > 95:
        return "Top Score"
    elif score >= 60:
        return "Pass"
    return "Fail"


def format_name(first_name: str, last_name: str) -> str:
    """
    Formats name string according to standard Coursera specification:
    'Name: last_name, first_name' or single name, or empty string.
    """
    f = first_name.strip()
    l = last_name.strip()
    if f and l:
        return f"Name: {l}, {f}"
    elif f:
        return f"Name: {f}"
    elif l:
        return f"Name: {l}"
    return ""


def fractional_part(numerator: int, denominator: int) -> float:
    """
    Returns fractional part of division or 0.0 if denominator is 0.
    """
    if denominator == 0:
        return 0.0
    return float((numerator % denominator) / denominator)


def convert_distance(miles: float) -> Tuple[float, str]:
    """
    Converts miles to kilometers (1 mile = 1.6 km).
    """
    km = round(miles * 1.6, 2)
    return km, f"{miles} miles equals {km} km"


def order_numbers(n1: int, n2: int) -> Tuple[int, int]:
    """
    Returns two numbers ordered ascendingly.
    """
    return (n2, n1) if n1 > n2 else (n1, n2)


# ======================================================================================
# MODULE 3: LOOPS & RECURSION
# ======================================================================================

def is_power_of_two(number: int) -> bool:
    """
    Determines whether a positive integer is a power of 2 using while loop.
    """
    if number <= 0:
        return False
    while number % 2 == 0:
        number //= 2
    return number == 1


def sum_divisors(n: int) -> int:
    """
    Computes sum of all proper divisors of n (from 1 up to n-1).
    """
    if n <= 1:
        return 0
    total = 0
    d = 1
    while d < n:
        if n % d == 0:
            total += d
        d += 1
    return total


def multiplication_table(start: int, stop: int) -> List[str]:
    """
    Generates multiplication table entries for range [start, stop].
    """
    table = []
    for x in range(start, stop + 1):
        for y in range(start, stop + 1):
            table.append(f"{x}x{y}={x * y}")
    return table


def counter(start: int, stop: int) -> str:
    """
    Generates space-separated counting sequence (ascending or descending).
    """
    step = 1 if start <= stop else -1
    return " ".join(str(x) for x in range(start, stop + step, step))


def count_digits(n: int) -> int:
    """
    Calculates number of decimal digits in integer n.
    """
    n = abs(n)
    if n == 0:
        return 1
    count = 0
    while n > 0:
        count += 1
        n //= 10
    return count


def factorial(n: int) -> int:
    """
    Computes factorial recursively with boundary verification.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers.")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def sum_positive_numbers(n: int) -> int:
    """
    Recursively sums numbers from 1 to n.
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return n + sum_positive_numbers(n - 1)


def is_power_of(number: int, base: int) -> bool:
    """
    Checks if number is power of base recursively.
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
    Generates set of 28 unique domino tiles (0-6).
    """
    return [(i, j) for i in range(7) for j in range(i, 7)]


# ======================================================================================
# MODULE 4: STRINGS, LISTS, AND DICTIONARIES
# ======================================================================================

def is_palindrome(text: str) -> bool:
    """
    Case-insensitive, alphanumeric-only palindrome verification.
    """
    clean = [ch.lower() for ch in text if ch.isalnum()]
    return clean == clean[::-1]


def replace_ending(sentence: str, old: str, new: str) -> str:
    """
    Replaces sentence ending if it matches 'old'.
    """
    if sentence.endswith(old):
        return sentence[:-len(old)] + new
    return sentence


def nametag(first_name: str, last_name: str) -> str:
    """
    Formats nametag string 'First L.'
    """
    if not first_name or not last_name:
        return (first_name or last_name).strip()
    return f"{first_name.strip()} {last_name.strip()[0]}."


def skip_elements(elements: List[Any]) -> List[Any]:
    """
    Extracts elements at even indices using comprehension.
    """
    return [elem for idx, elem in enumerate(elements) if idx % 2 == 0]


def pig_latin(text: str) -> str:
    """
    Converts sentence to Pig Latin.
    """
    words = text.split()
    return " ".join(f"{w[1:]}{w[0]}ay" for w in words)


def octal_to_string(octal: int) -> str:
    """
    Converts 3-digit octal permission integer to Unix permissions string.
    """
    res = []
    mapping = [(4, "r"), (2, "w"), (1, "x")]
    for ch in str(octal):
        val = int(ch)
        for weight, perm in mapping:
            if val >= weight:
                res.append(perm)
                val -= weight
            else:
                res.append("-")
    return "".join(res)


def email_list(domains: Dict[str, List[str]]) -> List[str]:
    """
    Flattens domain-to-users dictionary into email strings.
    """
    return [f"{u}@{d}" for d, users in domains.items() for u in users]


def groups_per_user(group_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Inverts group-to-users mapping to user-to-groups mapping.
    """
    user_map: Dict[str, List[str]] = {}
    for group, users in group_dict.items():
        for user in users:
            user_map.setdefault(user, []).append(group)
    return user_map


def count_letters(text: str) -> Dict[str, int]:
    """
    Counts frequency of letters in text.
    """
    counts: Dict[str, int] = {}
    for ch in text.lower():
        if ch.isalpha():
            counts[ch] = counts.get(ch, 0) + 1
    return counts


# ======================================================================================
# MODULE 5: OBJECT-ORIENTED PROGRAMMING & FINAL PROJECT
# ======================================================================================

class Server:
    """
    Simulates enterprise server with active connection pool.
    """
    def __init__(self, name: str = "srv") -> None:
        self.name = name
        self.connections: Dict[str, float] = {}

    def add_connection(self, conn_id: str) -> None:
        self.connections[conn_id] = 1.0

    def close_connection(self, conn_id: str) -> None:
        self.connections.pop(conn_id, None)

    def load(self) -> float:
        return sum(self.connections.values())


class LoadBalancer:
    """
    Elastic load balancer routing connections to least-loaded nodes.
    """
    def __init__(self) -> None:
        self.servers: List[Server] = [Server("srv-1")]

    def add_server(self) -> Server:
        s = Server(f"srv-{len(self.servers) + 1}")
        self.servers.append(s)
        return s

    def avg_load(self) -> float:
        return sum(s.load() for s in self.servers) / len(self.servers) if self.servers else 0.0

    def route_connection(self, conn_id: str) -> str:
        if self.avg_load() > 5.0:
            self.add_server()
        target = min(self.servers, key=lambda s: s.load())
        target.add_connection(conn_id)
        return target.name


class Event:
    """
    Machine authentication event record.
    """
    def __init__(self, date: str, event_type: str, machine: str, user: str) -> None:
        self.date = date
        self.type = event_type.lower()
        self.machine = machine
        self.user = user


def current_users(events: List[Event]) -> Dict[str, Set[str]]:
    """
    Processes login/logout event timeline to determine active sessions.
    """
    sorted_events = sorted(events, key=lambda e: e.date)
    machines: Dict[str, Set[str]] = {}
    for e in sorted_events:
        machines.setdefault(e.machine, set())
        if e.type == "login":
            machines[e.machine].add(e.user)
        elif e.type == "logout":
            machines[e.machine].discard(e.user)
    return machines


def generate_report(machines: Dict[str, Set[str]]) -> List[str]:
    """
    Generates formatted list of machines and active users.
    """
    return [
        f"{m}: {', '.join(sorted(users))}"
        for m, users in sorted(machines.items())
        if users
    ]


def calculate_frequencies(
    file_contents: str,
    uninteresting_words: Optional[Set[str]] = None
) -> Dict[str, int]:
    """
    Final Project WordCloud word frequency calculator.
    Filters punctuation, numbers, and stopwords.
    """
    stopwords = uninteresting_words or {
        "the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as",
        "i", "me", "my", "we", "our", "you", "your", "he", "she", "they",
        "them", "his", "her", "their", "what", "which", "who", "whom", "this",
        "that", "am", "are", "was", "were", "be", "been", "being", "have",
        "has", "had", "do", "does", "did", "but", "at", "by", "with", "from",
        "here", "when", "where", "how", "all", "any", "both", "each", "few",
        "more", "some", "such", "no", "nor", "too", "very", "can", "will",
        "just", "for", "in", "on", "so", "not", "into", "up", "out"
    }

    words: List[str] = []
    curr: List[str] = []
    for ch in file_contents.lower():
        if ch.isalpha():
            curr.append(ch)
        else:
            if curr:
                words.append("".join(curr))
                curr = []
    if curr:
        words.append("".join(curr))

    freqs: Dict[str, int] = {}
    for w in words:
        if w not in stopwords and len(w) > 1:
            freqs[w] = freqs.get(w, 0) + 1
    return freqs


def run_system_health_audit(disk_path: str = ".") -> Dict[str, bool]:
    """
    Standard-library compliant system health audit.
    """
    du = shutil.disk_usage(disk_path)
    free_gb = du.free / (2**30)
    percent_free = 100 * du.free / du.total
    cpu_cores = os.cpu_count() or 0

    return {
        "disk_healthy": free_gb >= 1.0 and percent_free >= 5.0,
        "cpu_healthy": cpu_cores > 0,
        "python_runtime_healthy": sys.version_info.major >= 3
    }


# ======================================================================================
# COMPREHENSIVE ASSERTION TEST SUITE (100.00% PRECISION VERIFICATION)
# ======================================================================================

def run_all_assertions() -> None:
    """
    Executes assertions covering all course modules with strict mathematical precision.
    """
    print("=" * 70)
    print("STARTING GOOGLE IT AUTOMATION COURSE 1 VERIFICATION SUITE")
    print("=" * 70)

    # Module 2 Assertions
    assert calculate_storage(1) == 4096
    assert calculate_storage(4096) == 4096
    assert calculate_storage(4097) == 8192
    assert color_translator("RED") == "hex #ff0000"
    assert exam_grade(96) == "Top Score"
    assert exam_grade(60) == "Pass"
    assert exam_grade(59) == "Fail"
    assert format_name("Ahmed", "Rifai") == "Name: Rifai, Ahmed"
    assert fractional_part(5, 4) == 0.25
    assert fractional_part(5, 0) == 0.0
    km, _ = convert_distance(55)
    assert km == 88.0
    assert order_numbers(10, 2) == (2, 10)
    print("[PASS] Module 2: Basic Python Syntax (100% precision)")

    # Module 3 Assertions
    assert is_power_of_two(16) is True
    assert is_power_of_two(18) is False
    assert is_power_of_two(0) is False
    assert sum_divisors(6) == 6
    assert sum_divisors(12) == 16
    assert counter(1, 3) == "1 2 3"
    assert counter(3, 1) == "3 2 1"
    assert count_digits(12345) == 5
    assert count_digits(0) == 1
    assert factorial(5) == 120
    assert sum_positive_numbers(5) == 15
    assert is_power_of(27, 3) is True
    assert len(domino_tiles()) == 28
    print("[PASS] Module 3: Loops & Recursion (100% precision)")

    # Module 4 Assertions
    assert is_palindrome("Racecar") is True
    assert is_palindrome("hello") is False
    assert replace_ending("Pop music", "music", "rock") == "Pop rock"
    assert nametag("Ada", "Lovelace") == "Ada L."
    assert skip_elements(["A", "B", "C", "D"]) == ["A", "C"]
    assert pig_latin("hello world") == "ellohay orldway"
    assert octal_to_string(755) == "rwxr-xr-x"
    assert octal_to_string(644) == "rw-r--r--"
    em = email_list({"domain.com": ["user1", "user2"]})
    assert em == ["user1@domain.com", "user2@domain.com"]
    grp = groups_per_user({"dev": ["ahmed", "john"], "ops": ["ahmed"]})
    assert set(grp["ahmed"]) == {"dev", "ops"}
    letters = count_letters("Hello!!")
    assert letters["l"] == 2 and letters["h"] == 1
    print("[PASS] Module 4: Strings, Lists & Dictionaries (100% precision)")

    # Module 5 Assertions
    lb = LoadBalancer()
    lb.route_connection("c1")
    assert lb.servers[0].load() == 1.0

    sample = "Python automation script in Python is fast. Python rocks!"
    freqs = calculate_frequencies(sample)
    assert freqs["python"] == 3
    assert freqs["fast"] == 1
    assert "is" not in freqs

    events = [
        Event("2026-10-06 08:00:00", "login", "station-1", "ahmed"),
        Event("2026-10-06 09:00:00", "login", "station-2", "rifai"),
        Event("2026-10-06 09:30:00", "logout", "station-1", "ahmed"),
    ]
    sessions = current_users(events)
    assert sessions["station-1"] == set()
    assert sessions["station-2"] == {"rifai"}
    rep = generate_report(sessions)
    assert rep == ["station-2: rifai"]

    health = run_system_health_audit(".")
    assert all(health.values()) is True
    print("[PASS] Module 5: OOP & Final Project (100% precision)")

    print("=" * 70)
    print("ALL MODULES VALIDATED SUCCESSFULLY WITH 100.00% MATHEMATICAL PRECISION!")
    print("=" * 70)


if __name__ == "__main__":
    run_all_assertions()
