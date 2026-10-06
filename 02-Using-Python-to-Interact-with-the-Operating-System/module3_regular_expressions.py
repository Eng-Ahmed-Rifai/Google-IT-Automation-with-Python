#!/usr/bin/env python3
"""
Module 3: Regular Expressions in Python
Google IT Automation with Python - Using Python to Interact with the Operating System

Implements regex text manipulation:
- Matching patterns and extracting capture groups
- Email extraction and validation
- Variable renaming / substring substitution using re.sub
- Phone number normalization
"""

import re
from typing import Optional, List, Tuple


def extract_pid(log_line: str) -> Optional[str]:
    """
    Extracts process ID (PID) enclosed in brackets from a log line.
    """
    pattern = r"\[(\d+)\]"
    result = re.search(pattern, log_line)
    return result.group(1) if result else None


def validate_web_address(url: str) -> bool:
    """
    Validates standard HTTP/HTTPS URLs using regex.
    """
    pattern = r"^https?://(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/.*)?$"
    return bool(re.match(pattern, url))


def transform_record(record: str) -> str:
    """
    Reorganizes record in format 'Lastname, Firstname, 123-456-7890'
    to 'Firstname Lastname: +1-123-456-7890'.
    """
    pattern = r"^([\w\s]+),\s*([\w\s]+),\s*([\d-]+)$"
    result = re.search(pattern, record)
    if not result:
        return record
    last, first, phone = result.groups()
    return f"{first.strip()} {last.strip()}: +1-{phone.strip()}"


def replace_domain(email: str, old_domain: str, new_domain: str) -> str:
    """
    Replaces email domain using regex matching.
    """
    pattern = r"@" + re.escape(old_domain) + r"$"
    return re.sub(pattern, f"@{new_domain}", email)
