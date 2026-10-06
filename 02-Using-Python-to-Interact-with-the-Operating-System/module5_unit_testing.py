#!/usr/bin/env python3
"""
Module 5: Testing in Python & Implementing Unit Testing
Google IT Automation with Python - Using Python to Interact with the Operating System

Implements employee email lookup, boundary handling, and unit testable routines:
- emails.py core logic with edge case handling
- Parameter verification and IndexError safety
- Missing employee handling returning 'No email address found'
"""

import sys
import csv
from typing import Dict, Optional


def load_email_directory(csv_path: str) -> Dict[str, str]:
    """
    Loads employee email directory from CSV.
    """
    directory: Dict[str, str] = {}
    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    name, email = row[0].strip(), row[1].strip()
                    directory[name.lower()] = email
    except FileNotFoundError:
        pass
    return directory


def find_email(email_dict: Dict[str, str], fullname: Optional[str]) -> str:
    """
    Finds email for the given fullname.
    Handles None or missing parameters gracefully.
    """
    if not fullname or not fullname.strip():
        return "Missing parameters"
    
    key = fullname.strip().lower()
    if email_dict.get(key):
        return email_dict.get(key)
    else:
        return "No email address found"


def safe_divide(a: float, b: float) -> Optional[float]:
    """
    Safely divides two numbers catching ZeroDivisionError.
    """
    try:
        return a / b
    except ZeroDivisionError:
        return None
