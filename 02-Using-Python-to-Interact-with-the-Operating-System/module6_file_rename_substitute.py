#!/usr/bin/env python3
"""
Module 6: Bash Scripting & Substring File Renaming
Google IT Automation with Python - Using Python to Interact with the Operating System

Implements file substring renaming automation:
- Finding files containing specific prefix/pattern (e.g., 'jane')
- Generating old/new filename pairs
- Renaming files using string.replace(old_substring, new_substring)
"""

import os
from typing import List, Tuple


def generate_rename_pairs(file_paths: List[str], old_sub: str, new_sub: str) -> List[Tuple[str, str]]:
    """
    Generates a list of (old_file, new_file) pairs for files containing old_sub.
    """
    pairs: List[Tuple[str, str]] = []
    for path in file_paths:
        if old_sub in path:
            new_path = path.replace(old_sub, new_sub)
            pairs.append((path, new_path))
    return pairs


def batch_rename_files(file_pairs: List[Tuple[str, str]], dry_run: bool = True) -> int:
    """
    Renames files based on generated pairs.
    If dry_run is True, actions are logged without filesystem mutations.
    """
    renamed_count = 0
    for old_name, new_name in file_pairs:
        if dry_run:
            renamed_count += 1
        else:
            if os.path.exists(old_name):
                os.rename(old_name, new_name)
                renamed_count += 1
    return renamed_count
