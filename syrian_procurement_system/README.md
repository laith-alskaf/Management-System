# نظام إدارة المشتريات الوطني السوري

##
نظام إدارة مشتريات وطني سوري - نسخة محلية لسطح المكتب.

##

- **تصميم عصري وجذاب:** واجهة مستخدم حديثة مع هوية بصرية سورية.
- **دعم كامل للغة العربية (RTL):** تجربة مستخدم طبيعية للناطقين بالعربية.
- **بنية MVC:** فصل واضح بين طبقات الكود لسهولة الصيانة والتطوير.
- **مصادقة Firebase:** نظام تسجيل دخول آمن وموثوق.
- **قاعدة بيانات محلية:** يعمل بشكل كامل دون اتصال بالإنترنت (باستثناء المصادقة).

##

- Python 3.10+
- PyQt6
- Requests
- ReportLab
- OpenPyxl
- SQLAlchemy

##

1. **استنساخ المستودع:**
   ```bash
   git clone https://github.com/your-username/syrian-procurement-system.git
   cd syrian-procurement-system
   ```

2. **إنشاء بيئة افتراضية (اختياري ولكن موصى به):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **تثبيت المتطلبات:**
   ```bash
   pip install -r syrian_procurement_system/requirements.txt
   ```

4. **إعداد Firebase:**
   - افتح ملف `syrian_procurement_system/config/firebase_config.py`.
   - استبدل القيم الوهمية (`YOUR_API_KEY`, `YOUR_PROJECT_ID`, etc.) بالقيم الحقيقية لمشروع Firebase الخاص بك.

5. **تشغيل التطبيق:**
   ```bash
   python syrian_procurement_system/main.py
   ```

##

نرحب بالمساهمات! يرجى اتباع الإرشادات القياسية لطلبات السحب (Pull Requests).

##

هذا المشروع مرخص بموجب ترخيص MIT.
