#!/usr/bin/env python3
"""
Module 7: Final Project - Log Analysis Using Regular Expressions
Google IT Automation with Python - Using Python to Interact with the Operating System

Implements complete log analysis and reporting pipeline:
- Parses syslog lines matching INFO and ERROR messages
- Tracks error type counts and per-user statistics (INFO vs ERROR count)
- Sorts error messages by frequency descending using operator.itemgetter(1)
- Sorts user statistics alphabetically by username using operator.itemgetter(0)
- Exports reports to CSV files and HTML tabular structures
"""

import re
import csv
import operator
from typing import Dict, List, Tuple, Any


def parse_syslog(log_lines: List[str]) -> Tuple[Dict[str, int], Dict[str, Dict[str, int]]]:
    """
    Parses syslog entries into error frequency dictionary and per-user statistics.
    Returns:
        errors: { "Error message string": count, ... }
        users: { "username": {"INFO": count, "ERROR": count}, ... }
    """
    errors: Dict[str, int] = {}
    users: Dict[str, Dict[str, int]] = {}

    pattern = r"ticky: (INFO|ERROR) ([\w ']+)(?: \[#\d+\])? \(([\w.]+)\)"

    for line in log_lines:
        match = re.search(pattern, line)
        if not match:
            continue

        log_type = match.group(1)
        message = match.group(2).strip()
        username = match.group(3).strip()

        if username not in users:
            users[username] = {"INFO": 0, "ERROR": 0}

        if log_type == "ERROR":
            errors[message] = errors.get(message, 0) + 1
            users[username]["ERROR"] += 1
        elif log_type == "INFO":
            users[username]["INFO"] += 1

    return errors, users


def sort_errors_by_frequency(errors: Dict[str, int]) -> List[Tuple[str, int]]:
    """
    Sorts error dictionary by occurrence count descending.
    """
    return sorted(errors.items(), key=operator.itemgetter(1), reverse=True)


def sort_users_alphabetically(users: Dict[str, Dict[str, int]]) -> List[Tuple[str, Dict[str, int]]]:
    """
    Sorts user dictionary alphabetically by username.
    """
    return sorted(users.items(), key=operator.itemgetter(0))


def export_errors_to_csv(sorted_errors: List[Tuple[str, int]], output_path: str) -> None:
    """
    Writes sorted error counts to CSV with headers 'Error', 'Count'.
    """
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Error", "Count"])
        for err, count in sorted_errors:
            writer.writerow([err, count])


def export_users_to_csv(sorted_users: List[Tuple[str, Dict[str, int]]], output_path: str) -> None:
    """
    Writes sorted user statistics to CSV with headers 'Username', 'INFO', 'ERROR'.
    """
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "INFO", "ERROR"])
        for user, stats in sorted_users:
            writer.writerow([user, stats["INFO"], stats["ERROR"]])


def convert_csv_to_html(csv_path: str) -> str:
    """
    Converts a CSV file into an HTML table markup string.
    """
    html_lines = ["<table>"]
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header:
            html_lines.append("  <tr>" + "".join(f"<th>{col}</th>" for col in header) + "</tr>")
        for row in reader:
            html_lines.append("  <tr>" + "".join(f"<td>{col}</td>" for col in row) + "</tr>")
    html_lines.append("</table>")
    return "\n".join(html_lines)
