#!/usr/bin/env python3
"""
Module 2: Managing Files and Directories with Python
Google IT Automation with Python - Using Python to Interact with the Operating System

Implements file handling, directory navigation, CSV parsing, and metadata inspection:
- os and os.path utilities
- CSV reading and writing with csv module
- File timestamp formatting
"""

import os
import csv
import datetime
from typing import List, Dict, Any


def create_sample_csv(filepath: str, data: List[Dict[str, Any]]) -> None:
    """
    Creates a CSV file from a list of dictionaries.
    """
    if not data:
        return
    fieldnames = list(data[0].keys())
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def read_csv_data(filepath: str) -> List[Dict[str, str]]:
    """
    Reads CSV rows into a list of dictionaries.
    """
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def get_file_metadata(filepath: str) -> Dict[str, Any]:
    """
    Returns file size and formatted modification timestamp.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    stat = os.stat(filepath)
    mod_time = datetime.datetime.fromtimestamp(stat.st_mtime)
    return {
        "size_bytes": stat.st_size,
        "modified_at": mod_time.strftime("%Y-%m-%d %H:%M:%S"),
        "is_file": os.path.isfile(filepath),
        "is_dir": os.path.isdir(filepath)
    }


def find_files_by_extension(directory: str, extension: str) -> List[str]:
    """
    Walks a directory and returns files ending with the specified extension.
    """
    matched = []
    if not os.path.exists(directory):
        return matched
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                matched.append(os.path.join(root, file))
    return matched
