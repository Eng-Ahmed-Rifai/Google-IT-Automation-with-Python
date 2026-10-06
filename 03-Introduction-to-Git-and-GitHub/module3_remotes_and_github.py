#!/usr/bin/env python3
"""
Module 3: Working with Remotes & GitHub Integration
Google IT Automation with Python - Introduction to Git and GitHub

Implements remote repository management:
- Parsing remote URLs (HTTPS vs SSH)
- Extracting owner and repository names from GitHub URLs
- Generating authenticated HTTPS clone URLs with Personal Access Tokens (PAT)
- Simulating fetch, pull, and push synchronization
"""

import re
from typing import Dict, Optional


def parse_github_url(url: str) -> Optional[Dict[str, str]]:
    """
    Parses a GitHub URL and extracts host, owner, and repository name.
    Supports both HTTPS (https://github.com/owner/repo.git)
    and SSH (git@github.com:owner/repo.git).
    """
    https_pattern = r"^https?://([^/]+)/([^/]+)/([^/.]+)(?:\.git)?$"
    ssh_pattern = r"^git@([^:]+):([^/]+)/([^/.]+)(?:\.git)?$"

    match = re.match(https_pattern, url)
    if match:
        return {"host": match.group(1), "owner": match.group(2), "repo": match.group(3), "protocol": "https"}

    match = re.match(ssh_pattern, url)
    if match:
        return {"host": match.group(1), "owner": match.group(2), "repo": match.group(3), "protocol": "ssh"}

    return None


def build_authenticated_url(url_info: Dict[str, str], username: str, pat_token: str) -> str:
    """
    Constructs an authenticated HTTPS URL embedding username and token.
    """
    host = url_info.get("host", "github.com")
    owner = url_info["owner"]
    repo = url_info["repo"]
    return f"https://{username}:{pat_token}@{host}/{owner}/{repo}.git"
