#!/usr/bin/env python3
"""
Module 2: Using Git Locally & Branching / Merging Workflows
Google IT Automation with Python - Introduction to Git and GitHub

Implements Git local workflow helpers:
- Branch creation and switching (git branch, git checkout, git switch)
- Fast-forward and 3-way merges (git merge)
- Detecting and resolving merge conflict markers (<<<<<<<, =======, >>>>>>>)
- Rolling back and undoing changes (git revert, git checkout --)
"""

import re
from typing import Dict, List, Tuple


def detect_conflict_markers(file_content: str) -> List[Dict[str, str]]:
    """
    Parses conflict markers in a file and extracts current vs incoming changes.
    Pattern:
    <<<<<<< HEAD
    current_content
    =======
    incoming_content
    >>>>>>> branch_name
    """
    pattern = r"<<<<<<< (.*?)\n(.*?)\n=======\n(.*?)\n>>>>>>> (.*?)(?:\n|$)"
    matches = re.findall(pattern, file_content, re.DOTALL)
    conflicts = []
    for match in matches:
        current_branch, current_code, incoming_code, incoming_branch = match
        conflicts.append({
            "current_branch": current_branch.strip(),
            "current_code": current_code.strip(),
            "incoming_code": incoming_code.strip(),
            "incoming_branch": incoming_branch.strip()
        })
    return conflicts


def resolve_conflict_favoring_incoming(file_content: str) -> str:
    """
    Automatically resolves merge conflicts by accepting incoming changes.
    """
    pattern = r"<<<<<<< .*?\n.*?\n=======\n(.*?)\n>>>>>>> .*?(?:\n|$)"
    return re.sub(pattern, r"\1\n", file_content, flags=re.DOTALL)
