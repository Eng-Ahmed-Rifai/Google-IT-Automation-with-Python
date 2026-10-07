"""
Google IT Automation with Python - Course 5: Configuration Management and the Cloud
Module 4: CI/CD Pipelines & Automated Rollback Strategies (module4_cicd_pipeline.py)

Covers:
- Continuous Integration & Continuous Deployment Pipeline Engine
- Automated Pipeline Stages (Linting, Unit Testing, Artifact Building, Deploying, Smoke Testing)
- Versioned Artifact Registry with SHA-256 Checksum Validation
- Automated Deployment Rollback on Health / Smoke Test Failure
"""

import enum
import hashlib
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


class StageStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class PipelineStage:
    """
    Represents an isolated stage in a CI/CD pipeline.
    """
    def __init__(self, name: str, action: Callable[[], bool]) -> None:
        self.name = name
        self.action = action
        self.status = StageStatus.PENDING
        self.error_message: Optional[str] = None
        self.duration_seconds: float = 0.0

    def execute(self) -> bool:
        self.status = StageStatus.RUNNING
        start_time = time.perf_counter()
        try:
            success = self.action()
            self.duration_seconds = time.perf_counter() - start_time
            if success:
                self.status = StageStatus.SUCCESS
                return True
            else:
                self.status = StageStatus.FAILED
                self.error_message = f"Stage '{self.name}' returned failure status."
                return False
        except Exception as ex:
            self.duration_seconds = time.perf_counter() - start_time
            self.status = StageStatus.FAILED
            self.error_message = str(ex)
            return False


class BuildArtifact:
    """
    Immutable versioned deployment package with checksum integrity.
    """
    def __init__(self, name: str, version: str, payload: str) -> None:
        self.name = name
        self.version = version
        self.payload = payload
        self.checksum = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self.created_at = time.time()


class ArtifactRegistry:
    """
    Central repository for versioned build artifacts.
    """
    def __init__(self) -> None:
        self.artifacts: Dict[str, BuildArtifact] = {}  # version -> artifact

    def publish(self, artifact: BuildArtifact) -> None:
        self.artifacts[artifact.version] = artifact

    def get_artifact(self, version: str) -> Optional[BuildArtifact]:
        return self.artifacts.get(version)


class DeploymentEnvironment:
    """
    Target production/staging environment hosting the live service.
    """
    def __init__(self, name: str = "production") -> None:
        self.name = name
        self.active_artifact: Optional[BuildArtifact] = None
        self.previous_artifact: Optional[BuildArtifact] = None
        self.deployment_history: List[str] = []

    def deploy(self, artifact: BuildArtifact) -> None:
        self.previous_artifact = self.active_artifact
        self.active_artifact = artifact
        self.deployment_history.append(f"Deployed {artifact.name}:{artifact.version}")

    def rollback(self) -> bool:
        """
        Reverts active environment to previous known-stable artifact.
        """
        if not self.previous_artifact:
            return False
        reverted_to = self.previous_artifact
        self.deployment_history.append(
            f"ROLLBACK: Reverted from {self.active_artifact.version if self.active_artifact else 'None'} to {reverted_to.version}"
        )
        self.active_artifact = reverted_to
        self.previous_artifact = None
        return True


class CICDPipelineRunner:
    """
    Orchestrates continuous integration and deployment with automated rollback.
    """
    def __init__(
        self,
        registry: ArtifactRegistry,
        environment: DeploymentEnvironment
    ) -> None:
        self.registry = registry
        self.environment = environment
        self.execution_audit: List[str] = []

    def run_pipeline(
        self,
        artifact_name: str,
        version: str,
        payload: str,
        test_suite_passes: bool = True,
        smoke_test_passes: bool = True
    ) -> Dict[str, Any]:
        """
        Executes standard pipeline workflow:
        1. Lint
        2. Test
        3. Build & Publish Artifact
        4. Deploy to Environment
        5. Smoke Test & Health Check (Triggers Rollback if failed)
        """
        candidate_artifact = BuildArtifact(artifact_name, version, payload)
        stages: List[PipelineStage] = []

        # 1. Lint Stage
        stages.append(PipelineStage("Lint Code", lambda: True))

        # 2. Test Stage
        stages.append(PipelineStage("Unit & Integration Tests", lambda: test_suite_passes))

        # 3. Build & Publish Stage
        def build_and_publish() -> bool:
            self.registry.publish(candidate_artifact)
            return True

        stages.append(PipelineStage("Package & Publish Artifact", build_and_publish))

        # 4. Deploy Stage
        def deploy_step() -> bool:
            self.environment.deploy(candidate_artifact)
            return True

        stages.append(PipelineStage("Deploy to Environment", deploy_step))

        # 5. Smoke Test Stage
        stages.append(PipelineStage("Post-Deploy Smoke Test", lambda: smoke_test_passes))

        # Execute stages sequentially
        pipeline_success = True
        failed_stage_name: Optional[str] = None
        rollback_triggered = False

        for i, stage in enumerate(stages):
            if not pipeline_success:
                stage.status = StageStatus.SKIPPED
                continue

            stage_ok = stage.execute()
            if not stage_ok:
                pipeline_success = False
                failed_stage_name = stage.name
                self.execution_audit.append(f"Stage '{stage.name}' FAILED.")

                # If failure happened after deployment (in smoke tests), execute automated rollback!
                if stage.name == "Post-Deploy Smoke Test":
                    rollback_ok = self.environment.rollback()
                    rollback_triggered = True
                    if rollback_ok:
                        self.execution_audit.append("Automated Rollback EXECUTED successfully.")
                    else:
                        self.execution_audit.append("Rollback FAILED: No previous artifact available.")

        return {
            "pipeline_success": pipeline_success,
            "failed_stage": failed_stage_name,
            "rollback_triggered": rollback_triggered,
            "active_version": self.environment.active_artifact.version if self.environment.active_artifact else None,
            "stages": [
                {"name": s.name, "status": s.status.value, "error": s.error_message}
                for s in stages
            ]
        }


def test_module4() -> None:
    """
    Validation assertion test suite for Module 4.
    """
    registry = ArtifactRegistry()
    env = DeploymentEnvironment("production")
    runner = CICDPipelineRunner(registry, env)

    # 1. Initial baseline stable release (v1.0.0)
    res_v1 = runner.run_pipeline("web-service", "v1.0.0", "stable_release_v1", test_suite_passes=True, smoke_test_passes=True)
    assert res_v1["pipeline_success"] is True
    assert res_v1["rollback_triggered"] is False
    assert res_v1["active_version"] == "v1.0.0"
    assert env.active_artifact.version == "v1.0.0"
    assert registry.get_artifact("v1.0.0") is not None
    assert all(s["status"] == "SUCCESS" for s in res_v1["stages"])

    # 2. Release with failing unit tests (v1.1.0) -> must halt at Test stage, skip deploy
    res_v1_fail = runner.run_pipeline("web-service", "v1.1.0", "buggy_code", test_suite_passes=False)
    assert res_v1_fail["pipeline_success"] is False
    assert res_v1_fail["failed_stage"] == "Unit & Integration Tests"
    assert env.active_artifact.version == "v1.0.0"  # Environment was untouched
    # Later stages must be SKIPPED
    stage_statuses = {s["name"]: s["status"] for s in res_v1_fail["stages"]}
    assert stage_statuses["Deploy to Environment"] == "SKIPPED"
    assert stage_statuses["Post-Deploy Smoke Test"] == "SKIPPED"

    # 3. Release that deploys but fails post-deploy smoke tests (v2.0.0-unstable) -> must trigger automated rollback to v1.0.0!
    res_rollback = runner.run_pipeline(
        "web-service",
        "v2.0.0-unstable",
        "broken_in_prod",
        test_suite_passes=True,
        smoke_test_passes=False
    )
    assert res_rollback["pipeline_success"] is False
    assert res_rollback["failed_stage"] == "Post-Deploy Smoke Test"
    assert res_rollback["rollback_triggered"] is True
    # The active environment must have reverted to v1.0.0!
    assert env.active_artifact.version == "v1.0.0"
    assert res_rollback["active_version"] == "v1.0.0"

    # 4. Artifact Checksum Integrity
    art = registry.get_artifact("v1.0.0")
    expected_hash = hashlib.sha256("stable_release_v1".encode("utf-8")).hexdigest()
    assert art.checksum == expected_hash

    print("[PASS] Module 4 (CI/CD Pipelines & Rollback): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module4()
