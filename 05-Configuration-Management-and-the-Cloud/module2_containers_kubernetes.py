"""
Google IT Automation with Python - Course 5: Configuration Management and the Cloud
Module 2: Containers & Kubernetes Orchestration (module2_containers_kubernetes.py)

Covers:
- Docker Container Lifecycle Simulation (create, start, stop, pause, inspect)
- Dockerfile Generation & Multi-Stage Build Validation
- Container Health Check Probes (STARTING, HEALTHY, UNHEALTHY)
- Kubernetes Manifest Models (Pod, Service, Deployment)
- Kubernetes Orchestration Simulator (Reconciliation loop, self-healing, rolling updates)
"""

import enum
import json
import uuid
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class ContainerState(enum.Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    DEAD = "DEAD"


class HealthState(enum.Enum):
    NONE = "NONE"
    STARTING = "STARTING"
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"


# -------------------------------------------------------------
# 1. DOCKERFILE GENERATOR & VALIDATOR
# -------------------------------------------------------------

class DockerfileBuilder:
    """
    Constructs and validates Dockerfiles according to best practices.
    """
    def __init__(self) -> None:
        self.instructions: List[Tuple[str, str]] = []

    def from_image(self, base_image: str, stage_name: Optional[str] = None) -> "DockerfileBuilder":
        arg = f"{base_image} AS {stage_name}" if stage_name else base_image
        self.instructions.append(("FROM", arg))
        return self

    def workdir(self, path: str) -> "DockerfileBuilder":
        self.instructions.append(("WORKDIR", path))
        return self

    def copy(self, src: str, dest: str, from_stage: Optional[str] = None) -> "DockerfileBuilder":
        arg = f"--from={from_stage} {src} {dest}" if from_stage else f"{src} {dest}"
        self.instructions.append(("COPY", arg))
        return self

    def run(self, command: str) -> "DockerfileBuilder":
        self.instructions.append(("RUN", command))
        return self

    def env(self, key: str, value: str) -> "DockerfileBuilder":
        self.instructions.append(("ENV", f"{key}={value}"))
        return self

    def expose(self, port: int) -> "DockerfileBuilder":
        self.instructions.append(("EXPOSE", str(port)))
        return self

    def entrypoint(self, cmd_list: List[str]) -> "DockerfileBuilder":
        formatted = json.dumps(cmd_list)
        self.instructions.append(("ENTRYPOINT", formatted))
        return self

    def cmd(self, cmd_list: List[str]) -> "DockerfileBuilder":
        formatted = json.dumps(cmd_list)
        self.instructions.append(("CMD", formatted))
        return self

    def build_dockerfile(self) -> str:
        """
        Validates structure and renders Dockerfile string.
        """
        if not self.instructions:
            raise ValueError("Dockerfile cannot be empty.")
        if self.instructions[0][0] != "FROM":
            raise ValueError("First instruction in Dockerfile must be FROM.")

        lines = [f"{op} {val}" for op, val in self.instructions]
        return "\n".join(lines)


# -------------------------------------------------------------
# 2. DOCKER CONTAINER LIFECYCLE & HEALTH CHECKS
# -------------------------------------------------------------

class Container:
    """
    Simulates a container instance with runtime attributes and logs.
    """
    def __init__(
        self,
        container_id: str,
        name: str,
        image: str,
        ports: Optional[Dict[int, int]] = None,
        environment: Optional[Dict[str, str]] = None
    ) -> None:
        self.container_id = container_id
        self.name = name
        self.image = image
        self.ports = ports or {}
        self.environment = environment or {}
        self.state = ContainerState.CREATED
        self.health_state = HealthState.NONE
        self.logs: List[str] = []
        self._consecutive_failures = 0
        self._consecutive_successes = 0

    def append_log(self, message: str) -> None:
        self.logs.append(message)


class ContainerEngine:
    """
    Simulates the local Docker daemon container runtime.
    """
    def __init__(self) -> None:
        self.containers: Dict[str, Container] = {}

    def create(
        self,
        name: str,
        image: str,
        ports: Optional[Dict[int, int]] = None,
        environment: Optional[Dict[str, str]] = None
    ) -> Container:
        container_id = str(uuid.uuid4())[:12]
        container = Container(container_id, name, image, ports, environment)
        self.containers[container_id] = container
        return container

    def start(self, container_id: str) -> None:
        c = self._get(container_id)
        if c.state in (ContainerState.CREATED, ContainerState.STOPPED):
            c.state = ContainerState.RUNNING
            c.append_log(f"Container {c.name} started.")

    def stop(self, container_id: str) -> None:
        c = self._get(container_id)
        if c.state in (ContainerState.RUNNING, ContainerState.PAUSED):
            c.state = ContainerState.STOPPED
            c.append_log(f"Container {c.name} stopped.")

    def pause(self, container_id: str) -> None:
        c = self._get(container_id)
        if c.state == ContainerState.RUNNING:
            c.state = ContainerState.PAUSED

    def unpause(self, container_id: str) -> None:
        c = self._get(container_id)
        if c.state == ContainerState.PAUSED:
            c.state = ContainerState.RUNNING

    def remove(self, container_id: str, force: bool = False) -> None:
        c = self._get(container_id)
        if c.state == ContainerState.RUNNING and not force:
            raise RuntimeError(f"Cannot remove running container {container_id} without force=True.")
        del self.containers[container_id]

    def update_health(
        self,
        container_id: str,
        probe_success: bool,
        failure_threshold: int = 3,
        success_threshold: int = 2
    ) -> HealthState:
        c = self._get(container_id)
        if c.state != ContainerState.RUNNING:
            return HealthState.NONE

        if probe_success:
            c._consecutive_successes += 1
            c._consecutive_failures = 0
            if c._consecutive_successes >= success_threshold or c.health_state == HealthState.NONE:
                c.health_state = HealthState.HEALTHY
        else:
            c._consecutive_failures += 1
            c._consecutive_successes = 0
            if c._consecutive_failures >= failure_threshold:
                c.health_state = HealthState.UNHEALTHY

        return c.health_state

    def _get(self, container_id: str) -> Container:
        if container_id not in self.containers:
            raise KeyError(f"Container '{container_id}' not found.")
        return self.containers[container_id]


# -------------------------------------------------------------
# 3. KUBERNETES MANIFEST BUILDER
# -------------------------------------------------------------

class KubernetesManifestBuilder:
    """
    Generates declarative Kubernetes resource definitions.
    """
    @staticmethod
    def create_pod_manifest(
        name: str,
        image: str,
        labels: Optional[Dict[str, str]] = None,
        port: int = 80
    ) -> Dict[str, Any]:
        return {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name,
                "labels": labels or {"app": name}
            },
            "spec": {
                "containers": [{
                    "name": name,
                    "image": image,
                    "ports": [{"containerPort": port}]
                }]
            }
        }

    @staticmethod
    def create_deployment_manifest(
        name: str,
        image: str,
        replicas: int = 3,
        app_label: str = "web",
        port: int = 80
    ) -> Dict[str, Any]:
        return {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": name},
            "spec": {
                "replicas": replicas,
                "selector": {"matchLabels": {"app": app_label}},
                "template": {
                    "metadata": {"labels": {"app": app_label}},
                    "spec": {
                        "containers": [{
                            "name": name,
                            "image": image,
                            "ports": [{"containerPort": port}]
                        }]
                    }
                }
            }
        }


# -------------------------------------------------------------
# 4. KUBERNETES ORCHESTRATION & ROLLING UPDATE SIMULATOR
# -------------------------------------------------------------

class K8sPod:
    """Simulates a Kubernetes Pod instance."""
    def __init__(self, pod_id: str, name: str, image: str, labels: Dict[str, str]) -> None:
        self.pod_id = pod_id
        self.name = name
        self.image = image
        self.labels = labels
        self.is_ready = True


class KubernetesClusterSimulator:
    """
    Simulates Kubernetes reconciliation loop, Pod self-healing, and Deployment Rolling Updates.
    """
    def __init__(self) -> None:
        self.pods: Dict[str, K8sPod] = {}
        self.deployments: Dict[str, Dict[str, Any]] = {}
        self._pod_counter = 0

    def apply_deployment(self, manifest: Dict[str, Any]) -> None:
        dep_name = manifest["metadata"]["name"]
        self.deployments[dep_name] = manifest
        self.reconcile(dep_name)

    def reconcile(self, dep_name: str) -> None:
        """
        Reconciliation loop: compares desired replicas with active pods,
        creating missing pods or terminating excess pods.
        """
        dep = self.deployments[dep_name]
        desired_replicas = dep["spec"]["replicas"]
        app_label = dep["spec"]["selector"]["matchLabels"]["app"]
        desired_image = dep["spec"]["template"]["spec"]["containers"][0]["image"]

        matching_pods = [
            p for p in self.pods.values()
            if p.labels.get("app") == app_label and p.is_ready
        ]

        # Self-healing: if pods are fewer than desired replicas
        if len(matching_pods) < desired_replicas:
            deficit = desired_replicas - len(matching_pods)
            for _ in range(deficit):
                self._pod_counter += 1
                pid = f"{dep_name}-{self._pod_counter}"
                new_pod = K8sPod(pid, pid, desired_image, {"app": app_label})
                self.pods[pid] = new_pod

        # Scale down if pods exceed desired replicas
        elif len(matching_pods) > desired_replicas:
            surplus = len(matching_pods) - desired_replicas
            for _ in range(surplus):
                to_remove = matching_pods.pop()
                del self.pods[to_remove.pod_id]

    def rolling_update(self, dep_name: str, new_image: str) -> List[str]:
        """
        Simulates a zero-downtime rolling update strategy:
        Incrementally replaces old pods with new pods having new_image.
        """
        dep = self.deployments[dep_name]
        dep["spec"]["template"]["spec"]["containers"][0]["image"] = new_image
        app_label = dep["spec"]["selector"]["matchLabels"]["app"]
        audit_log: List[str] = []

        old_pods = [
            p for p in list(self.pods.values())
            if p.labels.get("app") == app_label and p.image != new_image
        ]

        for old_pod in old_pods:
            # 1. Spin up replacement pod with new image
            self._pod_counter += 1
            new_pid = f"{dep_name}-{self._pod_counter}"
            new_pod = K8sPod(new_pid, new_pid, new_image, {"app": app_label})
            self.pods[new_pid] = new_pod
            audit_log.append(f"Started new pod {new_pid} with image {new_image}")

            # 2. Terminate old pod
            del self.pods[old_pod.pod_id]
            audit_log.append(f"Terminated old pod {old_pod.pod_id} running image {old_pod.image}")

        return audit_log


def test_module2() -> None:
    """
    Validation assertion test suite for Module 2.
    """
    # 1. DockerfileBuilder
    builder = DockerfileBuilder()
    df = (
        builder.from_image("python:3.11-slim", stage_name="base")
        .workdir("/app")
        .copy("requirements.txt", "./")
        .run("pip install --no-cache-dir -r requirements.txt")
        .copy(".", ".")
        .env("PORT", "8080")
        .expose(8080)
        .entrypoint(["python"])
        .cmd(["app.py"])
        .build_dockerfile()
    )
    assert "FROM python:3.11-slim AS base" in df
    assert "WORKDIR /app" in df
    assert "EXPOSE 8080" in df
    assert 'ENTRYPOINT ["python"]' in df

    # 2. Container Lifecycle & Health Checks
    engine = ContainerEngine()
    c = engine.create("web-app", "nginx:alpine", ports={80: 8080})
    assert c.state == ContainerState.CREATED

    engine.start(c.container_id)
    assert c.state == ContainerState.RUNNING

    engine.pause(c.container_id)
    assert c.state == ContainerState.PAUSED

    engine.unpause(c.container_id)
    assert c.state == ContainerState.RUNNING

    # Health check transitions
    h1 = engine.update_health(c.container_id, probe_success=True)
    assert h1 == HealthState.HEALTHY

    engine.update_health(c.container_id, probe_success=False)
    engine.update_health(c.container_id, probe_success=False)
    h_bad = engine.update_health(c.container_id, probe_success=False)
    assert h_bad == HealthState.UNHEALTHY

    engine.stop(c.container_id)
    assert c.state == ContainerState.STOPPED
    engine.remove(c.container_id)
    assert c.container_id not in engine.containers

    # 3. Kubernetes Manifests
    dep_manifest = KubernetesManifestBuilder.create_deployment_manifest("nginx-dep", "nginx:1.25", replicas=3)
    assert dep_manifest["kind"] == "Deployment"
    assert dep_manifest["spec"]["replicas"] == 3

    # 4. Kubernetes Simulator: Self-healing & Rolling Updates
    cluster = KubernetesClusterSimulator()
    cluster.apply_deployment(dep_manifest)
    assert len(cluster.pods) == 3

    # Simulate pod crash (kill one pod)
    killed_id = list(cluster.pods.keys())[0]
    del cluster.pods[killed_id]
    assert len(cluster.pods) == 2

    # Reconciliation loop must restore 3 pods
    cluster.reconcile("nginx-dep")
    assert len(cluster.pods) == 3

    # Rolling update
    update_log = cluster.rolling_update("nginx-dep", "nginx:1.26-alpine")
    assert len(update_log) == 6  # 3 started, 3 terminated
    assert all(p.image == "nginx:1.26-alpine" for p in cluster.pods.values())
    assert len(cluster.pods) == 3

    print("[PASS] Module 2 (Containers & Kubernetes): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module2()
