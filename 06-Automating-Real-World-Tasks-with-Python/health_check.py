"""
Google IT Automation with Python - Course 6: Automating Real-World Tasks with Python
Health Check Monitoring Script (health_check.py)

Monitors system metrics according to Coursera Lab 4 specifications:
1. CPU usage > 80% -> Alert: "Error - CPU usage is over 80%"
2. Available disk space < 20% -> Alert: "Error - Available disk space is less than 20%"
3. Available memory < 500MB -> Alert: "Error - Available memory is less than 500MB"
4. Hostname resolution of 'localhost' != '127.0.0.1' -> Alert: "Error - localhost cannot be resolved to 127.0.0.1"

Sends automated alert emails upon any threshold violation.
"""

import os
import shutil
import socket
import sys
import psutil
from typing import List, Optional

from module3_email_pdf import generate_email_message, send_email


def check_cpu_usage(threshold_percent: float = 80.0, interval: float = 0.1) -> bool:
    """
    Returns True if CPU usage is healthy (<= threshold), False if violated (> threshold).
    """
    usage = psutil.cpu_percent(interval=interval)
    return usage <= threshold_percent


def check_disk_space(disk_path: str = "/", min_free_percent: float = 20.0) -> bool:
    """
    Returns True if available disk space is >= min_free_percent, False if violated.
    """
    # Windows disk root normalization if default '/' doesn't exist
    target_path = disk_path if os.path.exists(disk_path) else "."
    du = shutil.disk_usage(target_path)
    percent_free = (du.free / du.total) * 100.0
    return percent_free >= min_free_percent


def check_memory(min_free_mb: float = 500.0) -> bool:
    """
    Returns True if available virtual memory is >= min_free_mb, False if violated.
    """
    vm = psutil.virtual_memory()
    available_mb = vm.available / (1024 * 1024)
    return available_mb >= min_free_mb


def check_localhost_resolution(expected_ip: str = "127.0.0.1") -> bool:
    """
    Returns True if 'localhost' resolves to expected_ip (127.0.0.1), False otherwise.
    """
    try:
        resolved_ip = socket.gethostbyname("localhost")
        return resolved_ip == expected_ip
    except Exception:
        return False


def run_system_health_audit(disk_path: str = ".") -> List[str]:
    """
    Executes all 4 health checks and returns a list of error alert subject lines for any violations.
    """
    errors: List[str] = []

    if not check_cpu_usage(threshold_percent=80.0):
        errors.append("Error - CPU usage is over 80%")

    if not check_disk_space(disk_path=disk_path, min_free_percent=20.0):
        errors.append("Error - Available disk space is less than 20%")

    if not check_memory(min_free_mb=500.0):
        errors.append("Error - Available memory is less than 500MB")

    if not check_localhost_resolution():
        errors.append("Error - localhost cannot be resolved to 127.0.0.1")

    return errors


def send_health_alert(
    subject: str,
    recipient: str = "username@example.com",
    sender: str = "automation@example.com",
    body: str = "Please check your system and resolve the issue as soon as possible.",
    simulate: bool = True
) -> bool:
    """
    Composes and sends an alert email for a specific health violation.
    """
    msg = generate_email_message(sender=sender, recipient=recipient, subject=subject, body=body)
    return send_email(msg, simulate=simulate)


def monitor_and_alert(
    recipient: str = "username@example.com",
    sender: str = "automation@example.com",
    disk_path: str = ".",
    simulate: bool = True
) -> int:
    """
    Runs full health audit, dispatches alert emails for each violated condition,
    and returns count of violations.
    """
    violations = run_system_health_audit(disk_path=disk_path)
    for error_subject in violations:
        send_health_alert(subject=error_subject, recipient=recipient, sender=sender, simulate=simulate)
    return len(violations)


def test_health_check() -> None:
    """
    Validation assertion test suite for health_check.py.
    """
    from unittest.mock import patch, MagicMock

    # 1. Test localhost resolution
    assert check_localhost_resolution() is True, "localhost did not resolve to 127.0.0.1"

    # 2. Test memory check with live system
    # Should evaluate without exception
    mem_ok = check_memory(min_free_mb=1.0)
    assert mem_ok is True

    # 3. Test CPU check with live system
    cpu_ok = check_cpu_usage(threshold_percent=100.0)
    assert cpu_ok is True

    # 4. Test Mocked Violations
    with patch("psutil.cpu_percent", return_value=95.0), \
         patch("shutil.disk_usage", return_value=MagicMock(free=10, total=100)), \
         patch("psutil.virtual_memory", return_value=MagicMock(available=200 * 1024 * 1024)), \
         patch("socket.gethostbyname", return_value="192.168.1.1"):

        violations = run_system_health_audit()
        assert len(violations) == 4
        assert "Error - CPU usage is over 80%" in violations
        assert "Error - Available disk space is less than 20%" in violations
        assert "Error - Available memory is less than 500MB" in violations
        assert "Error - localhost cannot be resolved to 127.0.0.1" in violations

    print("[PASS] Health Check Monitor: All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_health_check()
