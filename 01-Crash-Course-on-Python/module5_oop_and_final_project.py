"""
Google IT Automation with Python - Course 1: Crash Course on Python
Module 5: Object-Oriented Programming & Final Project

Covers:
- Object-Oriented Programming (Classes, Methods, State, Encapsulation)
- Server & LoadBalancer Architecture Simulation
- Final Project Component A: WordCloud Frequency Generator
- Final Project Component B: Event Processing & User Session Tracking
- Final Project Component C: System Automation & Health Check Utilities (Standard Library Compliant)
"""

import os
import sys
import shutil
from typing import Dict, List, Set, Optional, Tuple


# -------------------------------------------------------------
# OOP FOUNDATIONS: SERVER & LOAD BALANCER SIMULATION
# -------------------------------------------------------------

class Server:
    """
    Simulates a network server with dynamic connection handling.
    """
    def __init__(self, name: str = "server") -> None:
        self.name = name
        self.connections: Dict[str, float] = {}

    def add_connection(self, connection_id: str) -> None:
        """Adds a new connection with initial load."""
        self.connections[connection_id] = 1.0

    def close_connection(self, connection_id: str) -> None:
        """Closes an active connection."""
        if connection_id in self.connections:
            del self.connections[connection_id]

    def load(self) -> float:
        """Calculates total current load on this server."""
        return sum(self.connections.values())

    def __str__(self) -> str:
        return f"Server({self.name}, load={self.load():.1f}, conns={len(self.connections)})"


class LoadBalancer:
    """
    Distributes connections across an elastic pool of servers.
    """
    def __init__(self) -> None:
        self.servers: List[Server] = [Server("srv-1")]

    def add_server(self) -> Server:
        """Spins up a new server in the pool."""
        new_srv = Server(f"srv-{len(self.servers) + 1}")
        self.servers.append(new_srv)
        return new_srv

    def close_connection(self, connection_id: str) -> None:
        """Finds and closes connection across all servers."""
        for server in self.servers:
            if connection_id in server.connections:
                server.close_connection(connection_id)
                return

    def avg_load(self) -> float:
        """Calculates average load per server."""
        if not self.servers:
            return 0.0
        total_load = sum(s.load() for s in self.servers)
        return total_load / len(self.servers)

    def route_connection(self, connection_id: str) -> str:
        """Routes connection to server with lowest current load."""
        # Auto-scale if average load exceeds threshold
        if self.avg_load() > 5.0:
            self.add_server()

        least_loaded = min(self.servers, key=lambda s: s.load())
        least_loaded.add_connection(connection_id)
        return least_loaded.name


# -------------------------------------------------------------
# FINAL PROJECT COMPONENT A: WORDCLOUD FREQUENCY GENERATOR
# -------------------------------------------------------------

DEFAULT_STOPWORDS = {
    "the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i",
    "me", "my", "we", "our", "you", "your", "he", "she", "they", "them",
    "his", "her", "their", "what", "which", "who", "whom", "this", "that",
    "am", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "but", "at", "by", "with", "from", "here", "when",
    "where", "how", "all", "any", "both", "each", "few", "more", "some",
    "such", "no", "nor", "too", "very", "can", "will", "just", "for", "in",
    "on", "so", "not", "into", "up", "out"
}


def calculate_frequencies(
    file_contents: str,
    uninteresting_words: Optional[Set[str]] = None
) -> Dict[str, int]:
    """
    Calculates word frequencies for WordCloud generation.
    - Strips punctuation and digits
    - Normalizes case to lowercase
    - Filters stopwords
    - Returns dictionary of {word: count}
    """
    if uninteresting_words is None:
        stopwords = DEFAULT_STOPWORDS
    else:
        stopwords = {w.lower() for w in uninteresting_words}

    # Extract words containing only alphabetic characters
    clean_words = []
    current_word = []

    for char in file_contents.lower():
        if char.isalpha():
            current_word.append(char)
        else:
            if current_word:
                clean_words.append("".join(current_word))
                current_word = []
    if current_word:
        clean_words.append("".join(current_word))

    frequencies: Dict[str, int] = {}
    for word in clean_words:
        if word not in stopwords and len(word) > 1:
            frequencies[word] = frequencies.get(word, 0) + 1

    return frequencies


# -------------------------------------------------------------
# FINAL PROJECT COMPONENT B: EVENT PROCESSING (USER TRACKER)
# -------------------------------------------------------------

class Event:
    """
    Represents an authentication event on an enterprise workstation.
    """
    def __init__(self, date: str, event_type: str, machine: str, user: str) -> None:
        self.date = date  # Format: "YYYY-MM-DD HH:MM:SS"
        self.type = event_type.lower()  # "login" or "logout"
        self.machine = machine
        self.user = user

    def __repr__(self) -> str:
        return f"Event({self.date}, {self.type}, {self.machine}, {self.user})"


def get_event_date(event: Event) -> str:
    """Helper extraction function for chronological sorting."""
    return event.date


def current_users(events: List[Event]) -> Dict[str, Set[str]]:
    """
    Chronologically sorts events and tracks actively logged-in users per machine.
    """
    sorted_events = sorted(events, key=get_event_date)
    machines: Dict[str, Set[str]] = {}

    for event in sorted_events:
        if event.machine not in machines:
            machines[event.machine] = set()

        if event.type == "login":
            machines[event.machine].add(event.user)
        elif event.type == "logout":
            machines[event.machine].discard(event.user)

    return machines


def generate_report(machines: Dict[str, Set[str]]) -> List[str]:
    """
    Generates human-readable report lines for machines with active users.
    Format: 'machine_name: user1, user2'
    """
    report_lines: List[str] = []
    for machine, users in sorted(machines.items()):
        if users:
            user_list = ", ".join(sorted(users))
            report_lines.append(f"{machine}: {user_list}")
    return report_lines


# -------------------------------------------------------------
# FINAL PROJECT COMPONENT C: SYSTEM AUTOMATION UTILITIES
# -------------------------------------------------------------

def check_disk_usage(disk_path: str = ".", min_gb: float = 1.0, min_percent: float = 5.0) -> bool:
    """
    Checks if there is enough free disk space using standard library shutil.
    Returns True if healthy, False if critical.
    """
    du = shutil.disk_usage(disk_path)
    free_gb = du.free / (2**30)
    percent_free = 100 * du.free / du.total
    return free_gb >= min_gb and percent_free >= min_percent


def check_cpu_available() -> bool:
    """
    Verifies CPU cores are detectable and available via standard os library.
    """
    cpu_cnt = os.cpu_count()
    return cpu_cnt is not None and cpu_cnt > 0


def run_system_health_audit(disk_path: str = ".") -> Dict[str, bool]:
    """
    Runs unified system health audit using standard library.
    """
    return {
        "disk_healthy": check_disk_usage(disk_path),
        "cpu_healthy": check_cpu_available(),
        "python_runtime_healthy": sys.version_info.major >= 3
    }


def test_module5() -> None:
    """
    Validation assertion test suite for Module 5.
    """
    # 1. OOP Tests: Server & LoadBalancer
    lb = LoadBalancer()
    lb.route_connection("conn_1")
    lb.route_connection("conn_2")
    assert lb.servers[0].load() == 2.0
    lb.close_connection("conn_1")
    assert lb.servers[0].load() == 1.0

    # Auto-scaling test
    for i in range(10):
        lb.route_connection(f"batch_{i}")
    assert len(lb.servers) >= 2, "LoadBalancer failed to scale up"
    assert lb.avg_load() > 0.0

    # 2. WordCloud Frequency Generator
    sample_text = (
        "Python is an amazing language! Python is efficient, and Python is easy to learn. "
        "Automation with Python saves immense time."
    )
    freqs = calculate_frequencies(sample_text)
    assert freqs["python"] == 4, f"Expected python=4, got {freqs.get('python')}"
    assert freqs["saves"] == 1
    assert freqs["amazing"] == 1
    assert "is" not in freqs, "Stopword 'is' should have been filtered out"
    assert "and" not in freqs, "Stopword 'and' should have been filtered out"
    assert "with" not in freqs, "Stopword 'with' should have been filtered out"

    # 3. Event Processing & User Tracker
    events = [
        Event("2026-10-06 10:00:00", "login", "server_alpha", "ahmed"),
        Event("2026-10-06 10:15:00", "login", "server_beta", "sarah"),
        Event("2026-10-06 10:30:00", "login", "server_alpha", "tariq"),
        Event("2026-10-06 11:00:00", "logout", "server_alpha", "ahmed"),
        Event("2026-10-06 11:30:00", "logout", "server_beta", "sarah"),
    ]
    tracked = current_users(events)
    assert tracked["server_alpha"] == {"tariq"}
    assert tracked["server_beta"] == set()

    report = generate_report(tracked)
    assert len(report) == 1
    assert report[0] == "server_alpha: tariq"

    # 4. System Automation Helper Functions
    disk_ok = check_disk_usage(".", min_gb=0.1, min_percent=1.0)
    assert disk_ok is True, "Disk check failed"

    cpu_ok = check_cpu_available()
    assert cpu_ok is True, "CPU check failed"

    audit = run_system_health_audit(".")
    assert audit["disk_healthy"] is True
    assert audit["cpu_healthy"] is True
    assert audit["python_runtime_healthy"] is True

    print("[PASS] Module 5: All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module5()
