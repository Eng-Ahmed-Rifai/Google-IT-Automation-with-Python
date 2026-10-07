"""
Google IT Automation with Python - Course 5: Configuration Management and the Cloud
Module 1: Cloud Automation, IaC & Elastic Scaling (module1_automation_cloud.py)

Covers:
- Infrastructure as Code (IaC) declarative resource models
- VM Instance Lifecycle Management (PROVISIONING, RUNNING, STOPPED, TERMINATED)
- Elastic Auto-scaling engine with cooldown periods and capacity boundaries
- Configuration Drift Detection & Automated Remediation Planning
"""

import enum
import time
from typing import Any, Dict, List, Optional, Set, Tuple


class VMState(enum.Enum):
    PENDING = "PENDING"
    PROVISIONING = "PROVISIONING"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    TERMINATED = "TERMINATED"


class VMInstance:
    """
    Represents a cloud virtual machine instance provisioned via IaC.
    """
    def __init__(
        self,
        instance_id: str,
        instance_type: str = "e2-medium",
        zone: str = "us-central1-a",
        image: str = "ubuntu-2204-lts",
        tags: Optional[List[str]] = None
    ) -> None:
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.zone = zone
        self.image = image
        self.tags = set(tags or [])
        self.state = VMState.PENDING
        self.cpu_utilization: float = 0.0  # Percentage 0.0 - 100.0
        self.ip_address: Optional[str] = None
        self.metadata: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "instance_type": self.instance_type,
            "zone": self.zone,
            "image": self.image,
            "tags": sorted(list(self.tags)),
            "state": self.state.value,
            "cpu_utilization": self.cpu_utilization,
            "ip_address": self.ip_address,
            "metadata": self.metadata.copy()
        }


class CloudInstanceManager:
    """
    Manages cloud VM instances and their lifecycle transitions.
    """
    def __init__(self) -> None:
        self.instances: Dict[str, VMInstance] = {}
        self._ip_counter = 10

    def provision_instance(
        self,
        instance_id: str,
        instance_type: str = "e2-medium",
        zone: str = "us-central1-a",
        image: str = "ubuntu-2204-lts",
        tags: Optional[List[str]] = None
    ) -> VMInstance:
        if instance_id in self.instances and self.instances[instance_id].state != VMState.TERMINATED:
            raise ValueError(f"Instance '{instance_id}' already exists and is active.")

        instance = VMInstance(instance_id, instance_type, zone, image, tags)
        instance.state = VMState.PROVISIONING
        # Simulate IP assignment and transition to RUNNING
        instance.ip_address = f"10.240.0.{self._ip_counter}"
        self._ip_counter += 1
        instance.state = VMState.RUNNING
        self.instances[instance_id] = instance
        return instance

    def stop_instance(self, instance_id: str) -> None:
        instance = self._get_instance(instance_id)
        if instance.state == VMState.RUNNING:
            instance.state = VMState.STOPPED
            instance.cpu_utilization = 0.0

    def start_instance(self, instance_id: str) -> None:
        instance = self._get_instance(instance_id)
        if instance.state == VMState.STOPPED:
            instance.state = VMState.RUNNING

    def terminate_instance(self, instance_id: str) -> None:
        instance = self._get_instance(instance_id)
        instance.state = VMState.TERMINATED
        instance.ip_address = None
        instance.cpu_utilization = 0.0

    def get_active_instances(self) -> List[VMInstance]:
        return [inst for inst in self.instances.values() if inst.state == VMState.RUNNING]

    def _get_instance(self, instance_id: str) -> VMInstance:
        if instance_id not in self.instances:
            raise KeyError(f"Instance '{instance_id}' not found.")
        return self.instances[instance_id]


class AutoScaler:
    """
    Elastic auto-scaler engine that monitors cluster load and adjusts instance count.
    """
    def __init__(
        self,
        manager: CloudInstanceManager,
        min_instances: int = 1,
        max_instances: int = 5,
        target_cpu_percent: float = 70.0,
        cooldown_ticks: int = 2
    ) -> None:
        self.manager = manager
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.target_cpu_percent = target_cpu_percent
        self.cooldown_ticks = cooldown_ticks
        self._current_cooldown = 0
        self._scale_events: List[str] = []

    def evaluate_and_scale(self) -> str:
        """
        Evaluates active cluster load and executes scale-out or scale-in actions.
        """
        active = self.manager.get_active_instances()
        current_count = len(active)

        if self._current_cooldown > 0:
            self._current_cooldown -= 1
            return f"COOLDOWN (remaining: {self._current_cooldown})"

        # Ensure minimum capacity
        if current_count < self.min_instances:
            deficit = self.min_instances - current_count
            for i in range(deficit):
                new_id = f"auto-vm-{len(self.manager.instances) + 1}"
                self.manager.provision_instance(new_id)
            self._current_cooldown = self.cooldown_ticks
            action = f"SCALE_UP: Min capacity enforced (+{deficit})"
            self._scale_events.append(action)
            return action

        if not active:
            return "IDLE: No active instances"

        avg_cpu = sum(inst.cpu_utilization for inst in active) / current_count

        # Scale Up condition: average load exceeds target threshold
        if avg_cpu > self.target_cpu_percent and current_count < self.max_instances:
            new_id = f"auto-vm-{len(self.manager.instances) + 1}"
            self.manager.provision_instance(new_id)
            self._current_cooldown = self.cooldown_ticks
            action = f"SCALE_UP: High load ({avg_cpu:.1f}% > {self.target_cpu_percent}%)"
            self._scale_events.append(action)
            return action

        # Scale Down condition: average load is significantly below target (< 30%)
        if avg_cpu < (self.target_cpu_percent * 0.4) and current_count > self.min_instances:
            # Terminate the instance with lowest load
            to_remove = min(active, key=lambda inst: inst.cpu_utilization)
            self.manager.terminate_instance(to_remove.instance_id)
            self._current_cooldown = self.cooldown_ticks
            action = f"SCALE_DOWN: Low load ({avg_cpu:.1f}%), terminated {to_remove.instance_id}"
            self._scale_events.append(action)
            return action

        return "STEADY: Load within acceptable parameters"


class ConfigurationDriftDetector:
    """
    Detects configuration drift between declared Infrastructure as Code templates
    and live deployed system configurations, generating actionable remediation plans.
    """
    @staticmethod
    def detect_drift(
        desired_state: Dict[str, Any],
        actual_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculates diff between desired and actual configuration dictionaries.
        """
        missing_keys: Set[str] = set(desired_state.keys()) - set(actual_state.keys())
        unexpected_keys: Set[str] = set(actual_state.keys()) - set(desired_state.keys())
        modified_values: Dict[str, Tuple[Any, Any]] = {}

        common_keys = set(desired_state.keys()) & set(actual_state.keys())
        for k in common_keys:
            if desired_state[k] != actual_state[k]:
                modified_values[k] = (desired_state[k], actual_state[k])

        is_drifted = bool(missing_keys or unexpected_keys or modified_values)

        return {
            "is_drifted": is_drifted,
            "missing_keys": sorted(list(missing_keys)),
            "unexpected_keys": sorted(list(unexpected_keys)),
            "modified_values": modified_values
        }

    @staticmethod
    def generate_remediation_plan(drift_report: Dict[str, Any]) -> List[str]:
        """
        Translates configuration drift into idempotent remediation instructions.
        """
        if not drift_report["is_drifted"]:
            return ["No configuration drift detected. System state is converged."]

        plan: List[str] = []
        for key in drift_report["missing_keys"]:
            plan.append(f"CREATE: Re-apply missing resource/attribute '{key}' to match desired state.")

        for key in drift_report["unexpected_keys"]:
            plan.append(f"DELETE: Remove unmanaged / rogue configuration '{key}'.")

        for key, (desired, actual) in drift_report["modified_values"].items():
            plan.append(f"UPDATE: Reconcile '{key}' from '{actual}' to desired value '{desired}'.")

        return plan


def test_module1() -> None:
    """
    Validation assertion test suite for Module 1.
    """
    # 1. CloudInstanceManager lifecycle
    mgr = CloudInstanceManager()
    vm1 = mgr.provision_instance("web-1", instance_type="e2-standard-2", tags=["web", "frontend"])
    assert vm1.state == VMState.RUNNING
    assert vm1.ip_address == "10.240.0.10"
    assert "web" in vm1.tags

    mgr.stop_instance("web-1")
    assert vm1.state == VMState.STOPPED
    mgr.start_instance("web-1")
    assert vm1.state == VMState.RUNNING

    # 2. AutoScaler behavior
    scaler = AutoScaler(mgr, min_instances=2, max_instances=4, target_cpu_percent=75.0, cooldown_ticks=1)

    # Currently we have 1 active VM, min is 2 -> should scale up to meet min capacity
    action1 = scaler.evaluate_and_scale()
    assert "SCALE_UP" in action1
    assert len(mgr.get_active_instances()) == 2

    # High load trigger
    for inst in mgr.get_active_instances():
        inst.cpu_utilization = 85.0

    # During cooldown, it should report cooldown
    action_cd = scaler.evaluate_and_scale()
    assert "COOLDOWN" in action_cd

    # Now cooldown expired, evaluate high load
    action_high = scaler.evaluate_and_scale()
    assert "SCALE_UP" in action_high
    assert len(mgr.get_active_instances()) == 3

    # Low load trigger
    scaler._current_cooldown = 0
    for inst in mgr.get_active_instances():
        inst.cpu_utilization = 15.0
    action_low = scaler.evaluate_and_scale()
    assert "SCALE_DOWN" in action_low
    assert len(mgr.get_active_instances()) == 2

    # 3. Drift Detection & Remediation
    desired = {
        "nginx_version": "1.24.0",
        "port": 80,
        "worker_processes": 4,
        "ssl_enabled": True
    }
    actual = {
        "nginx_version": "1.20.1",   # Modified
        "port": 80,                  # Matching
        "ssl_enabled": True,         # Matching
        "debug_mode": True           # Unexpected rogue key
        # worker_processes is missing
    }

    report = ConfigurationDriftDetector.detect_drift(desired, actual)
    assert report["is_drifted"] is True
    assert report["missing_keys"] == ["worker_processes"]
    assert report["unexpected_keys"] == ["debug_mode"]
    assert "nginx_version" in report["modified_values"]
    assert report["modified_values"]["nginx_version"] == ("1.24.0", "1.20.1")

    plan = ConfigurationDriftDetector.generate_remediation_plan(report)
    assert len(plan) == 3
    assert any("worker_processes" in p for p in plan)
    assert any("debug_mode" in p for p in plan)
    assert any("nginx_version" in p for p in plan)

    # Test converged state
    converged_report = ConfigurationDriftDetector.detect_drift(desired, desired)
    assert converged_report["is_drifted"] is False
    converged_plan = ConfigurationDriftDetector.generate_remediation_plan(converged_report)
    assert "No configuration drift detected" in converged_plan[0]

    print("[PASS] Module 1 (Cloud Automation & IaC): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module1()
