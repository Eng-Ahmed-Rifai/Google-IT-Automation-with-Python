# Course 1: Crash Course on Python (Google IT Automation with Python)

<div dir="rtl" style="font-family: 'Dubai', 'Segoe UI', Tahoma, sans-serif; font-weight: 500; text-align: right; line-height: 1.8;">
تم إعداد هذا المستودع كمرجع قياسي شامل وعالي الدقة (100.00% Precision) لجميع متطلبات، دوال، ومشاريع <b>Course 1: Crash Course on Python</b> ضمن برنامج شهادة Google IT Automation with Python الاحترافية للمهندس أحمد الرفاعي.
</div>

---

## 📁 هيكل المستندات والملفات (Directory Architecture)

```
01-Crash-Course-on-Python/
├── module2_basic_syntax.py          # دوال التراكيب الأساسية والتحويلات والشروط وحساب كتل التخزين
├── module3_loops.py                 # حلقات التكرار (While/For/Nested) والتحكم والعودية (Recursion)
├── module4_data_structures.py       # هياكل البيانات (النصوص، القوائم، القواميس، List Comprehensions)
├── module5_oop_and_final_project.py # البرمجة كائنية التوجه، مشروع WordCloud، وتتبع جلسات الدخول
├── crash_course_reference.py        # سكريبت مرجعي موحد شامل لجميع الوحدات مع فحوصات Assertion
├── test_all_modules.py              # مشغل الاختبارات الموحد للتحقق من دقة التنفيذ بنسبة 100.00%
└── README.md                        # التوثيق الشامل وخطة الجودة
```

---

## 🛠️ محتويات الوحدات (Module Implementations)

### Module 2: Basic Python Syntax (`module2_basic_syntax.py`)
- **`calculate_storage(filesize)`**: حساب تخصيص كتل الملفات على أنظمة الملفات (4096-byte blocks) بدقة جبرية.
- **`color_translator(color)`**: ترجمة أسماء الألوان إلى Hexadecimal.
- **`exam_grade(score)`**: تقييم الدرجات الجامعية والشروط المنطقية.
- **`format_name(first_name, last_name)`**: معالجة وصياغة أسماء الأشخاص بجميع الحالات الجزئية.
- **`fractional_part(numerator, denominator)`**: حساب الجزء الكسري بدقة والتعامل مع القسمة على صفر.
- **`convert_distance(miles)`**: تحويل الأميال إلى كيلومترات وتنسيق المخرجات.
- **`order_numbers(n1, n2)`**: ترتيب الأعداد تصاعدياً.

### Module 3: Loops & Recursion (`module3_loops.py`)
- **`is_power_of_two(number)`**: التحقق من قوى العدد 2 بواسطة `while` loop ومعالجة القيم السالبة والصفر.
- **`sum_divisors(n)`**: حساب مجموع القواسم الصحيحة باستثناء العدد نفسه (Proper Divisors).
- **`multiplication_table(start, stop)`**: توليد جداول الضرب باستخدام الحلقات المتداخلة (Nested Loops).
- **`counter(start, stop)`**: عداد تصاعدي/تنازلي مرن.
- **`count_digits(n)`**: عد خانات الأرقام في النظام العشري رياضياً.
- **`factorial_iterative(n)` & `factorial_recursive(n)`**: حساب المضروب بالطريقتين التكرارية والعودية.
- **`sum_positive_numbers(n)`**: حساب مجموع الأعداد الطبيعية عودياً.
- **`is_power_of(number, base)`**: التحقق من الأسس والأساسات عودياً.
- **`domino_tiles()`**: توليد مجموعة أحجار الدومينو الثنائية (28 حجر).

### Module 4: Strings, Lists, and Dictionaries (`module4_data_structures.py`)
- **Strings**:
  - `is_palindrome`: فحص التناظر اللفظي متجاهلاً الفراغات وعلامات الترقيم وحالة الأحرف.
  - `replace_ending`: استبدال نهايات الجمل بدقة.
  - `nametag`, `initials`, `convert_distance_formatted`.
- **Lists**:
  - `skip_elements`: استخلاص العناصر عند المؤشرات الزوجية باستخدام List Comprehension.
  - `pig_latin`: تحويل النصوص إلى Pig Latin.
  - `octal_to_string`: تحويل أذونات يونكس الثمانية (مثل 755) إلى الصيغة القياسية (`rwxr-xr-x`).
  - `group_list`, `guest_list`, `squares`, `odd_numbers`.
- **Dictionaries**:
  - `email_list`: تفكيك قواميس النطاقات والمستخدمين إلى عناوين بريد إلكتروني.
  - `groups_per_user`: عكس الفهرس (Inverted Index) لربط كل مستخدم بمجموعاته.
  - `add_prices`, `count_letters`, `highlight_word`, `combine_guests`.

### Module 5: OOP & Final Project (`module5_oop_and_final_project.py`)
- **OOP Architecture**:
  - `Server` & `LoadBalancer`: محاكاة توزيع الأحمال الشبكية والتحجيم التلقائي (Auto-scaling).
- **Final Project Component A (WordCloud)**:
  - `calculate_frequencies(file_contents, uninteresting_words)`: خوارزمية تنظيف النصوص، استبعاد الكلمات الشائعة (Stopwords)، وحساب تكرار الكلمات لعرض سحابة الكلمات.
- **Final Project Component B (Event Tracker & Reporting)**:
  - `Event`, `current_users(events)`, `generate_report(machines)`: محاكاة ومعالجة سجلات تسجيل الدخول والخروج لمستخدمي الأنظمة وتوليد تقارير الأجهزة النشطة.
- **Final Project Component C (System Automation Helpers)**:
  - `check_disk_usage`, `check_cpu_available`, `run_system_health_audit`: أدوات فحص سلامة النظام المعتمدة على المكتبات القياسية لبايثون لضمان أعلى توافقية بيئية.

---

## 🧪 التحقق والاختبار (Verification & Test Execution)

لتشغيل حزمة الاختبارات الشاملة والتأكد من نجاح كافة الـ Assertions:

```powershell
python D:\STUDY\AI\Coursera\repos\Google-IT-Automation-with-Python\01-Crash-Course-on-Python\test_all_modules.py
```

### نتيجة الاختبار المعتمدة:
```
================================================================================
GOOGLE IT AUTOMATION WITH PYTHON - COURSE 1: CRASH COURSE ON PYTHON
COMPREHENSIVE TEST SUITE EXECUTION
================================================================================
[PASS] Module 2: Basic Python Syntax (100.00% precision)
[PASS] Module 3: Loops & Recursion (100.00% precision)
[PASS] Module 4: Strings, Lists & Dictionaries (100.00% precision)
[PASS] Module 5: OOP & Final Project (100.00% precision)
[PASS] Consolidated Reference Suite (100.00% precision)
================================================================================
SUMMARY: 5/5 test suites passed cleanly in 0.001s.
OVERALL PRECISION: 100.00%
================================================================================
```
