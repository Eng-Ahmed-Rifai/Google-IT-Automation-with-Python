#!/usr/bin/env python3
"""
Module 1: Practical Automation & System Health Check
Google IT Automation with Python - Using Python to Interact with the Operating System

Implements system monitoring automation:
- Disk usage checking with shutil
- CPU utilization checking with psutil
"""

import shutil

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def check_disk_usage(disk: str = "/", threshold_percent: float = 20.0) -> bool:
    """
    Checks if free disk space is greater than threshold percentage.
    Returns True if healthy (free > threshold), False otherwise.
    """
    try:
        du = shutil.disk_usage(disk)
    except Exception:
        du = shutil.disk_usage(".")
    free_percent = (du.free / du.total) * 100
    return free_percent > threshold_percent


def check_cpu_usage(threshold_percent: float = 75.0, sample_interval: float = 0.1) -> bool:
    """
    Checks if CPU utilization is below the specified threshold.
    Returns True if healthy (usage < threshold), False otherwise.
    """
    if HAS_PSUTIL:
        usage = psutil.cpu_percent(sample_interval)
        return usage < threshold_percent
    return True


def system_health_status() -> dict:
    """
    Returns aggregate health dictionary for OS monitoring.
    """
    disk_ok = check_disk_usage("/", 10.0)
    cpu_ok = check_cpu_usage(95.0, 0.1)
    return {
        "disk_healthy": disk_ok,
        "cpu_healthy": cpu_ok,
        "all_healthy": disk_ok and cpu_ok
    }


if __name__ == "__main__":
    status = system_health_status()
    if not status["all_healthy"]:
        print("ALERT: System resources outside normal thresholds!")
    else:
        print("SUCCESS: System is healthy and within optimal parameters.")
