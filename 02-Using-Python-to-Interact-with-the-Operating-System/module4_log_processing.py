#!/usr/bin/env python3
"""
Module 4: Managing Data and Processes / Working with Log Files
Google IT Automation with Python - Using Python to Interact with the Operating System

Implements log file parsing and process interactions:
- Reading large log streams line-by-line
- Filtering specific log types (e.g., CRON, ERROR)
- Parsing user activities from system logs
"""

import sys
import re
from typing import Dict, List


def filter_log_by_pattern(log_lines: List[str], pattern: str) -> List[str]:
    """
    Returns lines that match the given regular expression pattern.
    """
    regex = re.compile(pattern)
    return [line.strip() for line in log_lines if regex.search(line)]


def count_usernames_in_logs(log_lines: List[str]) -> Dict[str, int]:
    """
    Parses usernames from log lines matching USER (username) pattern.
    """
    pattern = r"USER \((\w+)\)"
    counts: Dict[str, int] = {}
    for line in log_lines:
        match = re.search(pattern, line)
        if match:
            user = match.group(1)
            counts[user] = counts.get(user, 0) + 1
    return counts
