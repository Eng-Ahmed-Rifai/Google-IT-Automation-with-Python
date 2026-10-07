# Course 5: Configuration Management and the Cloud (Google IT Automation with Python)

<div dir="rtl" style="font-family: 'Dubai', 'Segoe UI', Tahoma, sans-serif; font-weight: 500; text-align: right; line-height: 1.8;">
تم إعداد هذا المستودع كمرجع معماري وبرمجي متكامل وعالي الدقة (100.00% Precision) لجميع مفاهيم وتقنيات <b>إدارة التكوين (Configuration Management)، والأتمتة السحابية (Cloud Automation)، والحاويات وتوزيع الخدمات (Containers & Kubernetes)، وخطوط النشر المستمر (CI/CD Pipelines)</b> ضمن برنامج شهادة Google IT Automation with Python للمهندس أحمد الرفاعي.
</div>

---

## 🏗️ هيكل المستودع والملفات (Directory Architecture)

```
05-Configuration-Management-and-the-Cloud/
├── module1_automation_cloud.py       # الأتمتة السحابية، البنية ككود (IaC)، التوسع المرن، وكشف الانحراف
├── module2_containers_kubernetes.py  # دورة حياة Docker، بناء Dockerfile، وفاحصات الصحة، ومحاكي Kubernetes
├── module3_puppet_monitoring.py      # صياغة Puppet DSL، محرك التقارب التكراري (Idempotency)، وأنظمة المراقبة
├── module4_cicd_pipeline.py          # محرك خطوط CI/CD، سجل الحزم المعنونة، واستراتيجيات التراجع التلقائي
├── test_config_management.py         # حزمة اختبارات شاملة موحدة قائمة على unittest
└── README.md                         # الدليل المعماري الشامل ومرجع الاستخدام
```

---

## 📘 تفصيل الوحدات البرمجية والأنماط المعمارية (Module Deep Dive)

### Module 1: Cloud Automation & Infrastructure as Code (`module1_automation_cloud.py`)
- **Infrastructure as Code (IaC)**:
  - نمذجة الموارد السحابية بشكل تصريحي (Declarative Resource Specifications).
  - إدارة دورة حياة الآلات الافتراضية: `PROVISIONING` -> `RUNNING` -> `STOPPED` -> `TERMINATED`.
- **Elastic AutoScaler**:
  - مراقبة متوسط استهلاك المعالج للمجموعة السحابية والتوسع التلقائي صعوداً (`Scale Out`) أو هبوطاً (`Scale In`).
  - تطبيق فترات التهدئة (`Cooldown Periods`) وحدود السعة الدنيا والقصوى لمنع التذبذب المفرط (Thrashing).
- **Configuration Drift Detection & Remediation**:
  - مقارنة الحالة المرغوبة (`Desired State`) مع الحالة الواقعية للنظام (`Actual Live State`).
  - تحديد المفاتيح المفقودة، والقيم المعدلة، والمفاتيح الزائدة المتسللة.
  - توليد خطة علاجية ذاتية (`Idempotent Remediation Plan`).

---

### Module 2: Containers & Kubernetes Orchestration (`module2_containers_kubernetes.py`)
- **Dockerfile Generator & Multi-stage Builder**:
  - التحقق من توافق تعليمات Dockerfile (`FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV`, `EXPOSE`, `ENTRYPOINT`, `CMD`).
  - دعم البناء متعدد المراحل (`Multi-stage builds`) لتقليص حجم الحزم النهائية.
- **Container Lifecycle & Health Probes**:
  - محاكاة محرك Docker Daemon وحالات الحاويات: `CREATED`, `RUNNING`, `PAUSED`, `STOPPED`.
  - مجسات الفحص الصحي (`Liveness / Readiness Probes`) مع عتبات الإخفاق المتتابع والتحول بين `STARTING`, `HEALTHY`, `UNHEALTHY`.
- **Kubernetes Orchestration & Rolling Updates**:
  - توليد مواصفات Pods و Deployments و Services المتوافقة مع مواصفات K8s.
  - حلقة المطابقة (`Reconciliation Loop`): التعافي الذاتي (`Self-healing`) واستبدال الحاويات المنهارة فورياً.
  - محاكاة التحديث التدريجي بدون انقطاع الخدمة (`Zero-Downtime Rolling Update`).

---

### Module 3: Puppet DSL & System Monitoring (`module3_puppet_monitoring.py`)
- **Puppet DSL Engine**:
  - بناء وتفكيك لغة Puppet التصريحية للموارد: `package`, `file`, `service`, `user`.
  - إدارة العلاقات والتبعيات: `require`, `notify`.
- **Idempotent Convergence Simulator**:
  - ضمان التطابق التكراري: تطبيق الإعدادات لا يُحدث أي تغييرات إذا كانت الحالة الحالية مطابقة للحالة المرغوبة (`0 changes / No-op`).
  - إطلاق إشعارات إعادة تشغيل الخدمات (`Service Reloads`) تلقائياً فقط عند تعديل ملفات التكوين.
- **Monitoring & Alerting Pipeline**:
  - تخزين السلاسل الزمنية للمقاييس وحساب المتوسطات المتحركة.
  - محرك قواعد التنبيه بمستويات `WARNING` و `CRITICAL` مع تعافٍ تلقائي عند عودة المؤشرات للمستويات الطبيعية.

---

### Module 4: CI/CD Pipelines & Rollback Strategies (`module4_cicd_pipeline.py`)
- **CI/CD Pipeline Engine**:
  - مراحل آلية متعاقبة: فحص التنسيق (`Lint`), الاختبارات (`Unit/Integration Tests`), بناء الحزم (`Build`), النشر (`Deploy`), واختبارات الدخان (`Smoke Tests`).
  - الإيقاف الفوري والتخطي الذكي للمراحل اللاحقة عند فشل أي خطوة مبكرة.
- **Immutable Artifact Registry**:
  - حزم إصدارات برمجية غير قابلة للتعديل محمية بترميز التجزئة الرياضي `SHA-256`.
- **Automated Rollback Engine**:
  - الكشف التلقائي عن فشل اختبارات ما بعد النشر وتفعيل التراجع الفوري إلى الإصدار المستقر السابق دون تدخل بشري.

---

## 🧪 نتائج الاختبار وضمان الجودة (Test Execution & Precision)

تم فحص كامل المستودع عبر مشغل الاختبارات الموحد:

```powershell
python D:\STUDY\AI\Coursera\repos\Google-IT-Automation-with-Python\05-Configuration-Management-and-the-Cloud\test_config_management.py
```

### التقرير المعتمد (Test Summary):
```
test_autoscaler_min_capacity_and_load (__main__.TestModule1CloudAutomation) ... ok
test_configuration_drift_and_remediation (__main__.TestModule1CloudAutomation) ... ok
test_vm_provisioning_and_lifecycle (__main__.TestModule1CloudAutomation) ... ok
test_container_lifecycle_and_probes (__main__.TestModule2ContainersKubernetes) ... ok
test_dockerfile_builder (__main__.TestModule2ContainersKubernetes) ... ok
test_kubernetes_orchestration_and_rolling_update (__main__.TestModule2ContainersKubernetes) ... ok
test_monitoring_alerts (__main__.TestModule3PuppetMonitoring) ... ok
test_puppet_dsl_and_idempotency (__main__.TestModule3PuppetMonitoring) ... ok
test_smoke_failure_triggers_automatic_rollback (__main__.TestModule4CICDPipeline) ... ok
test_successful_pipeline_deployment (__main__.TestModule4CICDPipeline) ... ok
test_test_failure_aborts_pipeline (__main__.TestModule4CICDPipeline) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.003s

OK
```

<div dir="rtl" style="font-family: 'Dubai', 'Segoe UI', Tahoma, sans-serif; font-weight: 500; text-align: right; line-height: 1.8;">
نسبة النجاح: <b>100.00%</b> عبر جميع وحدات واختبارات Course 5.
</div>
