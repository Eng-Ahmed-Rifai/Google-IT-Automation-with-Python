# Course 6: Automating Real-World Tasks with Python (Google IT Automation with Python)

<div dir="rtl" style="font-family: 'Dubai', 'Segoe UI', Tahoma, sans-serif; font-weight: 500; text-align: right; line-height: 1.8;">
تم إعداد هذا المستودع كمرجع تطبيقي متكامل وعالي الدقة (100.00% Precision) لجميع المشاريع الواقعية في <b>Course 6: Automating Real-World Tasks with Python</b> (المشروع الختامي / Capstone Course) ضمن برنامج شهادة Google IT Automation with Python للمهندس أحمد الرفاعي.
</div>

---

## 🏗️ هيكل المستودع والملفات (Directory Architecture)

```
06-Automating-Real-World-Tasks-with-Python/
├── module1_image_processing.py      # معالجة الصور بالدفعات (Pillow): تغيير الأبعاد، التدوير، والتحويل إلى JPEG
├── module2_web_services.py          # تكامل خدمات الويب (Requests): قراءة التقييمات، تحويلها لـ JSON، ورفعها مع إعادة المحاولة
├── module3_email_pdf.py             # توليد تقارير PDF احترافية (ReportLab) وإرسال البريد الإلكتروني الآلي (smtplib)
├── module4_catalog_automation.py    # خط معالجة كتالوج المنتجات: معالجة الصور، استخراج الأوزان، ورفع البيانات
├── health_check.py                  # نظام مراقبة صحة الخادم (CPU, Disk, Memory, DNS) وإرسال تنبيهات الطوارئ
├── test_real_world_automation.py    # حزمة الاختبارات الشاملة (unittest) المعتمدة بنسبة 100.00%
└── README.md                        # الدليل التوثيقي الشامل
```

---

## 🛠️ تفصيل المشاريع الواقعية (Real-World Modules Breakdown)

### 1. معالجة وتعديل الصور بالدفعات (`module1_image_processing.py`)
- **المكتبة**: `PIL` (Pillow).
- **المهام**:
  - فحص المجلدات واستخراج ملفات الصور المختلفة (`TIFF`, `PNG`, `RGBA`, `Grayscale`).
  - معالجة قنوات الألوان وتحويلها بأمان إلى `RGB` (مع إزالة قناة الشفافية Alpha دون تشوهات).
  - تدوير الصور 90 درجة باتجاه عقارب الساعة (`Clockwise`).
  - توحيد أبعاد الصور إلى `128x128` بكسل باستخدام مرشح `LANCZOS` عالي الجودة.
  - الحفظ بصيغة `JPEG` في مجلد الإخراج المنظم.

---

### 2. التفاعل مع خدمات الويب وواجهات البرمجة (`module2_web_services.py`)
- **المكتبة**: `requests`, `json`.
- **المهام**:
  - قراءة ملفات تقييمات العملاء النصية غير المهيكلة (`title`, `name`, `date`, `feedback`).
  - تحويل البيانات إلى قواميس Python مهيكلة ومتوافقة مع `JSON`.
  - التفاعل مع خوادم الويب عبر طلبات `HTTP POST` مع تفعيل استراتيجية إعادة المحاولة التدريجية (`Exponential Backoff`) في حال واجه الخادم أخطاء مؤقتة (`5xx`).

---

### 3. توليد التقارير وتوزيع البريد الإلكتروني آلياً (`module3_email_pdf.py`)
- **المكتبات**: `reportlab`, `email.message`, `smtplib`.
- **المهام**:
  - تحليل بيانات مبيعات السيارات وحساب مؤشرات الأعمال:
    - الطراز الأكثر تحقيقاً للإيرادات (`Most Revenue`).
    - الطراز الأكثر مبيعاً (`Most Sales`).
    - سنة الصنع الأكثر شعبية وإجمالي مبيعاتها (`Most Popular Year`).
  - بناء مستندات PDF منسقة بدقة تتضمن جداول بيانات ملونة وفق هوية Google Blue ونصوصاً تلخيصية (`SimpleDocTemplate`, `Table`, `Paragraph`).
  - إنشاء رسائل بريد إلكتروني متعددة الوسائط (`MIME`) وإرفاق ملفات الـ PDF مع التعرف التلقائي على نوع المرفق (`mimetypes`) ودعم وضع المحاكاة الآمن (`simulate=True`).

---

### 4. أتمتة كتالوج الموردين ونظام مراقبة الخادم (`module4_catalog_automation.py` & `health_check.py`)
- **مشروع الكتالوج**:
  - معالجة صور الفواكه وتغيير حجمها إلى `600x400` وحفظها بصيغة `.jpeg`.
  - تحليل ملفات الأوصاف وتحويل وزن الثمار (مثل `"500 lbs"`) إلى قيم عددية صحيحة (`int: 500`).
  - ربط كل وصف بالصورة المقابلة ورفع البيانات والصور عبر واجهات REST إلى الخادم.
- **نظام مراقبة الخادم (`health_check.py`)**:
  - **مراقبة المعالج**: تنبيه في حال تجاوز الاستهلاك 80% (`CPU usage > 80%`).
  - **مراقبة القرص**: تنبيه في حال انخفاض المساحة المتاحة عن 20% (`Disk space < 20%`).
  - **مراقبة الذاكرة**: تنبيه في حال انخفاض الذاكرة الحرة عن 500 ميجابايت (`Available memory < 500MB`).
  - **مراقبة دقة النطاق**: التأكد من مطابقة `localhost` للعنوان `127.0.0.1`.
  - إرسال رسائل بريد إلكتروني فورية للمسؤول عند حدوث أي تجاوز للمحددات.

---

## 🧪 نتائج الاختبار وضمان الجودة (Test Verification & Precision)

تم تنفيذ حزمة الاختبارات الشاملة المعتمدة `test_real_world_automation.py`:

```powershell
python D:\STUDY\AI\Coursera\repos\Google-IT-Automation-with-Python\06-Automating-Real-World-Tasks-with-Python\test_real_world_automation.py
```

### التقرير المعتمد (Test Summary):
```
test_batch_process_images (__main__.TestModule1ImageProcessing.test_batch_process_images) ... ok
test_process_single_image (__main__.TestModule1ImageProcessing.test_process_single_image) ... ok
test_parse_feedback_file (__main__.TestModule2WebServices.test_parse_feedback_file) ... ok
test_post_feedback_to_api_retries_on_500 (__main__.TestModule2WebServices.test_post_feedback_to_api_retries_on_500) ... ok
test_post_feedback_to_api_success (__main__.TestModule2WebServices.test_post_feedback_to_api_success) ... ok
test_generate_pdf_and_email_with_attachment (__main__.TestModule3EmailPDF.test_generate_pdf_and_email_with_attachment) ... ok
test_process_car_sales_data (__main__.TestModule3EmailPDF.test_process_car_sales_data) ... ok
test_parse_catalog_description (__main__.TestModule4CatalogAutomation.test_parse_catalog_description) ... ok
test_process_catalog_image (__main__.TestModule4CatalogAutomation.test_process_catalog_image) ... ok
test_health_check_violations_alerting (__main__.TestHealthCheck.test_health_check_violations_alerting) ... ok
test_localhost_resolution (__main__.TestHealthCheck.test_localhost_resolution) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.546s

OK (11/11 passed)
Overall Precision: 100.00%
```

<div dir="rtl" style="font-family: 'Dubai', 'Segoe UI', Tahoma, sans-serif; font-weight: 500; text-align: right; line-height: 1.8;">
نسبة النجاح: <b>100.00%</b> عبر جميع الاختبارات الـ 11 لكامل وحدات الدورة السادسة والختامية.
</div>
