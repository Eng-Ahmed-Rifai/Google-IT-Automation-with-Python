#!/usr/bin/env python3
"""
Module 1: Introduction to Version Control & Git Fundamentals
Google IT Automation with Python - Introduction to Git and GitHub

Implements Git automation helpers:
- Initializing new repositories (git init)
- Managing configuration (git config --global / --local)
- Tracking file state changes and staging area (git status, git add)
- Creating snapshots with formatted commit messages (git commit -m)
"""

import subprocess
import os
from typing import Dict, List, Optional, Any


def run_git_command(args: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
    """
    Executes a Git command safely via subprocess.
    """
    cmd = ["git"] + args
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "exit_code": result.returncode
    }


def parse_git_status_porcelain(status_output: str) -> Dict[str, List[str]]:
    """
    Parses 'git status --porcelain' output into categorized file lists:
    - staged: files ready for commit
    - unstaged: tracked files with unstaged changes
    - untracked: files not yet added to Git
    """
    categorized = {
        "staged": [],
        "unstaged": [],
        "untracked": []
    }
    for line in status_output.splitlines():
        if len(line) < 3:
            continue
        index_status = line[0]
        worktree_status = line[1]
        filename = line[3:].strip()

        if index_status in ["M", "A", "D", "R", "C"]:
            categorized["staged"].append(filename)
        if worktree_status in ["M", "D"]:
            categorized["unstaged"].append(filename)
        if index_status == "?" and worktree_status == "?":
            categorized["untracked"].append(filename)

    return categorized
