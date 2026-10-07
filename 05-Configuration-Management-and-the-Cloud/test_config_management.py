"""
Google IT Automation with Python - Course 5: Configuration Management and the Cloud
Comprehensive Test Suite (test_config_management.py)

Validates all 4 modules with 100.00% precision using unittest:
- TestModule1CloudAutomation
- TestModule2ContainersKubernetes
- TestModule3PuppetMonitoring
- TestModule4CICDPipeline
"""

import hashlib
import sys
import unittest

import module1_automation_cloud as m1
import module2_containers_kubernetes as m2
import module3_puppet_monitoring as m3
import module4_cicd_pipeline as m4


class TestModule1CloudAutomation(unittest.TestCase):
    """Validation test suite for Module 1: Cloud Automation, IaC & Auto-Scaling"""

    def setUp(self):
        self.mgr = m1.CloudInstanceManager()

    def test_vm_provisioning_and_lifecycle(self):
        vm = self.mgr.provision_instance("node-1", instance_type="e2-standard-4", tags=["api", "prod"])
        self.assertEqual(vm.state, m1.VMState.RUNNING)
        self.assertIsNotNone(vm.ip_address)
        self.assertIn("api", vm.tags)

        # Stop VM
        self.mgr.stop_instance("node-1")
        self.assertEqual(vm.state, m1.VMState.STOPPED)
        self.assertEqual(vm.cpu_utilization, 0.0)

        # Start VM
        self.mgr.start_instance("node-1")
        self.assertEqual(vm.state, m1.VMState.RUNNING)

        # Terminate VM
        self.mgr.terminate_instance("node-1")
        self.assertEqual(vm.state, m1.VMState.TERMINATED)
        self.assertIsNone(vm.ip_address)

    def test_autoscaler_min_capacity_and_load(self):
        scaler = m1.AutoScaler(self.mgr, min_instances=2, max_instances=5, target_cpu_percent=70.0, cooldown_ticks=0)
        # Should scale up immediately to meet min 2 instances
        action = scaler.evaluate_and_scale()
        self.assertIn("SCALE_UP", action)
        self.assertEqual(len(self.mgr.get_active_instances()), 2)

        # Set high load on all instances
        for inst in self.mgr.get_active_instances():
            inst.cpu_utilization = 88.0

        action_scale_high = scaler.evaluate_and_scale()
        self.assertIn("SCALE_UP", action_scale_high)
        self.assertEqual(len(self.mgr.get_active_instances()), 3)

        # Set low load
        for inst in self.mgr.get_active_instances():
            inst.cpu_utilization = 10.0

        action_scale_low = scaler.evaluate_and_scale()
        self.assertIn("SCALE_DOWN", action_scale_low)
        self.assertEqual(len(self.mgr.get_active_instances()), 2)

    def test_configuration_drift_and_remediation(self):
        desired = {"port": 443, "ssl": True, "workers": 8, "env": "prod"}
        actual = {"port": 80, "ssl": True, "debug": True}  # port changed, env & workers missing, debug extra

        report = m1.ConfigurationDriftDetector.detect_drift(desired, actual)
        self.assertTrue(report["is_drifted"])
        self.assertEqual(report["missing_keys"], ["env", "workers"])
        self.assertEqual(report["unexpected_keys"], ["debug"])
        self.assertEqual(report["modified_values"]["port"], (443, 80))

        plan = m1.ConfigurationDriftDetector.generate_remediation_plan(report)
        self.assertEqual(len(plan), 4)
        self.assertTrue(any("CREATE: Re-apply missing" in p for p in plan))
        self.assertTrue(any("DELETE: Remove unmanaged" in p for p in plan))
        self.assertTrue(any("UPDATE: Reconcile 'port'" in p for p in plan))


class TestModule2ContainersKubernetes(unittest.TestCase):
    """Validation test suite for Module 2: Containers & Kubernetes Orchestration"""

    def test_dockerfile_builder(self):
        builder = m2.DockerfileBuilder()
        df = (
            builder.from_image("golang:1.22-alpine", stage_name="build")
            .workdir("/src")
            .copy(".", ".")
            .run("go build -o server .")
            .from_image("alpine:latest")
            .copy("/src/server", "/usr/local/bin/server", from_stage="build")
            .expose(8080)
            .cmd(["/usr/local/bin/server"])
            .build_dockerfile()
        )
        self.assertIn("FROM golang:1.22-alpine AS build", df)
        self.assertIn("COPY --from=build /src/server /usr/local/bin/server", df)
        self.assertIn("EXPOSE 8080", df)

    def test_container_lifecycle_and_probes(self):
        engine = m2.ContainerEngine()
        cnt = engine.create("api-srv", "node:20-slim", ports={3000: 3000})
        self.assertEqual(cnt.state, m2.ContainerState.CREATED)

        engine.start(cnt.container_id)
        self.assertEqual(cnt.state, m2.ContainerState.RUNNING)

        # Probes: Healthy
        h = engine.update_health(cnt.container_id, probe_success=True)
        self.assertEqual(h, m2.HealthState.HEALTHY)

        # Failures threshold
        engine.update_health(cnt.container_id, probe_success=False)
        engine.update_health(cnt.container_id, probe_success=False)
        h_dead = engine.update_health(cnt.container_id, probe_success=False)
        self.assertEqual(h_dead, m2.HealthState.UNHEALTHY)

        engine.stop(cnt.container_id)
        self.assertEqual(cnt.state, m2.ContainerState.STOPPED)

    def test_kubernetes_orchestration_and_rolling_update(self):
        cluster = m2.KubernetesClusterSimulator()
        dep = m2.KubernetesManifestBuilder.create_deployment_manifest("cart-service", "cart:v1", replicas=4, app_label="cart")
        cluster.apply_deployment(dep)

        self.assertEqual(len(cluster.pods), 4)
        self.assertTrue(all(p.image == "cart:v1" for p in cluster.pods.values()))

        # Rolling update to cart:v2
        logs = cluster.rolling_update("cart-service", "cart:v2")
        self.assertEqual(len(logs), 8)  # 4 started, 4 terminated
        self.assertEqual(len(cluster.pods), 4)
        self.assertTrue(all(p.image == "cart:v2" for p in cluster.pods.values()))


class TestModule3PuppetMonitoring(unittest.TestCase):
    """Validation test suite for Module 3: Puppet DSL & System Monitoring"""

    def test_puppet_dsl_and_idempotency(self):
        manifest_text = """
package { 'apache2':
  ensure => 'installed',
}

file { '/var/www/html/index.html':
  ensure => 'file',
  content => '<h1>Welcome</h1>',
  mode => '0644',
  notify => Service['apache2'],
}

service { 'apache2':
  ensure => 'running',
  enable => true,
}
"""
        resources = m3.PuppetManifestEngine.parse_manifest(manifest_text)
        self.assertEqual(len(resources), 3)

        system = m3.SimulatedSystemState()
        engine = m3.PuppetIdempotencyEngine(system)

        # Run 1: Applies all 3 resources and triggers notification
        res1 = engine.apply_resources(resources)
        self.assertEqual(res1["changes_applied"], 3)
        self.assertFalse(res1["is_converged"])
        self.assertIn("Service['apache2']", system.service_reloads)

        # Run 2: Exact idempotency (0 changes applied)
        res2 = engine.apply_resources(resources)
        self.assertEqual(res2["changes_applied"], 0)
        self.assertEqual(res2["noop_count"], 3)
        self.assertTrue(res2["is_converged"])

    def test_monitoring_alerts(self):
        monitor = m3.MonitoringSystem()
        disk_rule = m3.MetricAlertRule("disk_usage_percent", warning_threshold=80.0, critical_threshold=90.0)
        monitor.add_rule(disk_rule)

        monitor.record_metric("disk_usage_percent", 70.0)
        self.assertEqual(disk_rule.current_severity, m3.AlertSeverity.OK)

        monitor.record_metric("disk_usage_percent", 82.0)
        self.assertEqual(disk_rule.current_severity, m3.AlertSeverity.WARNING)

        monitor.record_metric("disk_usage_percent", 92.5)
        self.assertEqual(disk_rule.current_severity, m3.AlertSeverity.CRITICAL)

        self.assertEqual(len(monitor.alert_log), 2)


class TestModule4CICDPipeline(unittest.TestCase):
    """Validation test suite for Module 4: CI/CD Pipeline & Automated Rollback"""

    def setUp(self):
        self.registry = m4.ArtifactRegistry()
        self.env = m4.DeploymentEnvironment("staging")
        self.runner = m4.CICDPipelineRunner(self.registry, self.env)

    def test_successful_pipeline_deployment(self):
        res = self.runner.run_pipeline("auth-service", "v1.0", "binary_v1_payload")
        self.assertTrue(res["pipeline_success"])
        self.assertFalse(res["rollback_triggered"])
        self.assertEqual(self.env.active_artifact.version, "v1.0")

        # Checksum check
        art = self.registry.get_artifact("v1.0")
        expected_chk = hashlib.sha256("binary_v1_payload".encode("utf-8")).hexdigest()
        self.assertEqual(art.checksum, expected_chk)

    def test_test_failure_aborts_pipeline(self):
        # Establish baseline first
        self.runner.run_pipeline("auth-service", "v1.0", "payload_v1")

        # Deploy failing tests
        res_fail = self.runner.run_pipeline("auth-service", "v1.1", "bad_payload", test_suite_passes=False)
        self.assertFalse(res_fail["pipeline_success"])
        self.assertEqual(res_fail["failed_stage"], "Unit & Integration Tests")
        self.assertEqual(self.env.active_artifact.version, "v1.0")  # Untouched

    def test_smoke_failure_triggers_automatic_rollback(self):
        # Baseline
        self.runner.run_pipeline("auth-service", "v1.0", "payload_v1")
        self.assertEqual(self.env.active_artifact.version, "v1.0")

        # New release deploys but fails smoke tests
        res_smoke_fail = self.runner.run_pipeline(
            "auth-service", "v2.0", "faulty_runtime_payload",
            test_suite_passes=True,
            smoke_test_passes=False
        )
        self.assertFalse(res_smoke_fail["pipeline_success"])
        self.assertTrue(res_smoke_fail["rollback_triggered"])
        self.assertEqual(res_smoke_fail["failed_stage"], "Post-Deploy Smoke Test")
        # Rollback restores v1.0
        self.assertEqual(self.env.active_artifact.version, "v1.0")
        self.assertEqual(res_smoke_fail["active_version"], "v1.0")


def run_full_suite() -> int:
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestModule1CloudAutomation))
    suite.addTests(loader.loadTestsFromTestCase(TestModule2ContainersKubernetes))
    suite.addTests(loader.loadTestsFromTestCase(TestModule3PuppetMonitoring))
    suite.addTests(loader.loadTestsFromTestCase(TestModule4CICDPipeline))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_full_suite())
