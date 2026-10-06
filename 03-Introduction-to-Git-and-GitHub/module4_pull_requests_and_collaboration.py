#!/usr/bin/env python3
"""
Module 4: Collaboration, Pull Requests & Code Reviews
Google IT Automation with Python - Introduction to Git and GitHub

Implements collaborative workflows:
- Formatting structured commit messages with issue references (Closes #123)
- Generating pull request templates with description, summary, and test checklists
- Simulating upstream remote tracking for forked repositories
"""

from typing import Dict, List, Optional, Any


def format_commit_message(summary: str, details: Optional[str] = None, closes_issue: Optional[int] = None) -> str:
    """
    Formats a Git commit message following industry best practices:
    - 50-char imperative summary line
    - Blank separator line
    - Detailed explanation of what and why
    - Optional issue closure trailer (e.g. Closes #42)
    """
    message_lines = [summary.strip()]
    if details:
        message_lines.append("")
        message_lines.append(details.strip())
    if closes_issue:
        if not details:
            message_lines.append("")
        message_lines.append(f"Closes #{closes_issue}")
    return "\n".join(message_lines)


def generate_pr_summary(title: str, feature_desc: str, changes: List[str], tested: bool = True) -> Dict[str, Any]:
    """
    Generates a structured Pull Request payload.
    """
    checklist = "- [x] All automated tests pass\n- [x] Code reviewed against project standards" if tested else "- [ ] Pending test suite verification"
    changes_formatted = "\n".join(f"* {c}" for c in changes)
    body = f"## Description\n{feature_desc}\n\n## Changes\n{changes_formatted}\n\n## Verification\n{checklist}"
    return {
        "title": title,
        "body": body,
        "ready_to_merge": tested
    }
