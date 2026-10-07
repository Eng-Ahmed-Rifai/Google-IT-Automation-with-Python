# Course 4: Troubleshooting and Debugging Techniques (Google IT Automation with Python)

<div dir="rtl" style="font-family: 'Dubai', 'Segoe UI', Tahoma, sans-serif; font-weight: 500; text-align: right; line-height: 1.8;">
تم إعداد هذا المستودع كمرجع هندسي متكامل ومختبر برمجي عالي الدقة (100.00% Precision) لجميع تقنيات ومنهجيات استكشاف الأخطاء وإصلاحها وحل المشكلات المعقدة في بيئات التشغيل، ضمن برنامج شهادة Google IT Automation with Python للمهندس أحمد الرفاعي.
</div>

---

## 🧭 منهجية استكشاف الأخطاء وإصلاحها (Troubleshooting Methodology)

<div dir="rtl" style="font-family: 'Dubai', 'Segoe UI', Tahoma, sans-serif; font-weight: 500; text-align: right; line-height: 1.8;">
تعتمد دورة Google المنهج العلمي الرباعي لحل المشكلات التقنية:
</div>

1. **إعادة إنتاج الخطأ (Reproduce)**: إنشاء حالة اختبار مصغرة ومعزولة تظهر المشكلة بشكل متكرر وموثوق.
2. **عزل نطاق الخطأ (Isolate)**: تضييق نطاق الكود أو البيانات المشبوهة باستخدام أسلوب التنصيف (Binary Bisection / Delta Debugging).
3. **تحديد السبب الجذري (Root Cause Identification)**: فحص مسار الاستدعاءات (Traceback) وتحليل استهلاك الموارد لاكتشاف الخلل الأصلي وليس مجرد الأعراض.
4. **الإصلاح والتحقق (Fix & Verify)**: تطبيق الحل الأنسب وإجراء اختبارات انحدار (Regression Tests) للتأكد من عدم حدوث آثار جانبية.

---

## 📁 هيكل المستودع والملفات (Directory Architecture)

```
04-Troubleshooting-and-Debugging-Techniques/
├── module1_debugging.py             # عزل الأخطاء، التحويل الآمن للأنواع، وتدقيق السجلات
├── module2_performance_tuning.py    # أدوات القياس (Profiling)، التوازي (Multiprocessing)، والبحث الثنائي
├── module3_crash_resolution.py      # تحليل مسارات الانهيار، تسريبات الذاكرة، والتكرار اللانهائي
├── module4_resource_management.py   # مراقبة الموارد، عمليات القرص المتدفقة، وإدارة العمليات والمهل
├── test_troubleshooting.py          # حزمة اختبارات unittest شاملة ومفصلة لجميع الوحدات
└── README.md                        # الدليل الهندسي الشامل والمنهجية
```

---

## 🛠️ محتويات الوحدات البرمجية (Module Breakdown)

### Module 1: Debugging & Error Isolation (`module1_debugging.py`)
- **`safe_cast(val, target_type, default)`**: تحويل آمن للأنواع (`int`, `float`, `bool`, `str`) مع معالجة النصوص المنطقية (`yes`, `no`, `true`, `false`) دون إطلاق استثناءات غير متوقعة.
- **`parse_and_validate_record(raw_data, schema)`**: التحقق من صحة السجلات وقواميس الإدخال ومطابقتها للمخطط المحدد مع تسجيل دقيق للأخطاء.
- **`bisect_failing_record(records, predicate)`**: خوارزمية البحث النصفي/الخطي لتحديد السجل المتسبب في عطل النظام (Delta Debugging).
- **`isolate_log_errors(log_lines, severity_levels)`**: استخراج وتصنيف رسائل الخطأ الحرجة من السجلات النصية.
- **`isolate_bug_causes(target_func, inputs)`**: تحليل مجمّع لحالات الاختبار وتصنيف الاستثناءات حسب نوعها.

### Module 2: Performance Tuning & Optimization (`module2_performance_tuning.py`)
- **`binary_search(sorted_items, target)` vs `linear_search`**:
  - مقارنة خوارزمية برمجية ورياضية تثبت تقليص عدد العمليات من $O(N)$ إلى $O(\log_2 N)$.
- **`profile_execution(func, *args)`**: تحليل أداء الدوال باستخدام `cProfile` وتوليد تقرير استدعاءات تفصيلي وتحديد عنق الزجاجة (Bottlenecks).
- **`memoize(func)`**: نمط التخزين المؤقت (Caching) لتفادي تكرار الحسابات الثقيلة.
- **`run_parallel_batch(inputs, max_workers)`**: معالجة دفعات المهام الحسابية بالتوازي باستخدام `ProcessPoolExecutor` لتسخير أنوية المعالج بالكامل مع التراجع الآمن للوضع المتسلسل.

### Module 3: Crash Resolution & Root Cause Investigation (`module3_crash_resolution.py`)
- **`parse_traceback_string(tb_text)`**: تحليل وتفكيك شجرة الأخطاء (Traceback) من الأسفل للأعلى وتحديد نوع الخطأ وموقعه وسطر السبب الجذري.
- **`capture_exception_info(func, *args)`**: تنفيذ آمن للدوال واعتراض وتحليل الاستثناءات البرمجية.
- **`MemoryLeakTracker`**: محاكاة وتتبع تسريبات الذاكرة الناتجة عن احتجاز المراجع غير المحدودة، ونظام تخزين مقيد بسعة قصوى وسياسة استبعاد (Eviction).
- **`guarded_recursive_traversal` & `iterative_tree_count`**: حماية مسارات العودية (Recursion Guard) وتحويل العودية العميقة إلى مكدس تكراري لتفادي `RecursionError`.
- **`recover_corrupt_json(raw_payload, default_fallback)`**: التعافي الذاتي من حمولات البيانات المشوهة أو الفاسدة مع وضع احتياطي آمن.

### Module 4: Resource Management & Process Lifecycle (`module4_resource_management.py`)
- **`process_file_in_chunks(filepath, chunk_size)`**: قراءة ومعالجة الملفات الضخمة ككتل ثنائية متدفقة لمنع استنزاف ذاكرة الوصول العشوائي (RAM).
- **`atomic_write_file(filepath, content)`**: الكتابة الذرية الآمنة للملفات عبر ملفات مؤقتة واستبدال نظامي لمنع تشوه الملفات عند انقطاع النظام، مع دعم كامل للبيئات المتعددة.
- **`check_disk_threshold(path, min_free_gb, min_percent)`**: مراقبة مساحة التخزين المتبقية والتحقق من سلامة البيئة.
- **`run_process_with_timeout(command, timeout_seconds)`**: تشغيل الأوامر الخارجية والعمليات الفرعية مع مهلة زمنية إشرافية تمنع العمليات المعلقة (Zombie / Hung Processes).
- **`ResourcePool` & `ManagedResourceContext`**: إدارة مجمعات الموارد المقيدة (Resource Pool) باستخدام سياقات `with` لضمان إرجاع الموارد بعد الاستخدام أو عند الخطأ.

---

## 🧪 نتائج الاختبار وضمان الجودة (Test Execution & Precision)

تم فحص جميع الوحدات بواسطة حزمة الاختبارات الشاملة `test_troubleshooting.py`:

```powershell
python D:\STUDY\AI\Coursera\repos\Google-IT-Automation-with-Python\04-Troubleshooting-and-Debugging-Techniques\test_troubleshooting.py
```

### التقرير المعتمد (Test Summary):
```
test_bisect_failing_record (__main__.TestModule1Debugging) ... ok
test_isolate_bug_causes (__main__.TestModule1Debugging) ... ok
test_isolate_log_errors (__main__.TestModule1Debugging) ... ok
test_parse_and_validate_record (__main__.TestModule1Debugging) ... ok
test_safe_cast_booleans (__main__.TestModule1Debugging) ... ok
test_safe_cast_defaults (__main__.TestModule1Debugging) ... ok
test_safe_cast_numerics (__main__.TestModule1Debugging) ... ok
test_binary_search_missing_element (__main__.TestModule2PerformanceTuning) ... ok
test_binary_search_vs_linear_search (__main__.TestModule2PerformanceTuning) ... ok
test_memoize_decorator (__main__.TestModule2PerformanceTuning) ... ok
test_profile_execution (__main__.TestModule2PerformanceTuning) ... ok
test_run_parallel_batch (__main__.TestModule2PerformanceTuning) ... ok
test_capture_exception_info (__main__.TestModule3CrashResolution) ... ok
test_memory_leak_tracker (__main__.TestModule3CrashResolution) ... ok
test_parse_traceback_string (__main__.TestModule3CrashResolution) ... ok
test_recover_corrupt_json (__main__.TestModule3CrashResolution) ... ok
test_recursion_guard_and_iterative_tree (__main__.TestModule3CrashResolution) ... ok
test_atomic_file_write_and_chunked_read (__main__.TestModule4ResourceManagement) ... ok
test_check_disk_threshold (__main__.TestModule4ResourceManagement) ... ok
test_resource_pool_lifecycle (__main__.TestModule4ResourceManagement) ... ok
test_run_process_with_timeout (__main__.TestModule4ResourceManagement) ... ok

----------------------------------------------------------------------
Ran 21 tests in 1.301s

OK
```
<div dir="rtl" style="font-family: 'Dubai', 'Segoe UI', Tahoma, sans-serif; font-weight: 500; text-align: right; line-height: 1.8;">
نسبة النجاح: <b>100.00%</b> عبر جميع الاختبارات الـ 21 بدون أي إخفاق.
</div>
