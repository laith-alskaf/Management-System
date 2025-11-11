# -*- coding: utf-8 -*-

"""
وحدة التحكم الخاصة بالمصادقة (Authentication Controller)
"""

from syrian_procurement_system.services.firebase_service import FirebaseService
from syrian_procurement_system.views.auth_views.login_view import LoginView

class AuthController:
    """
    فئة وحدة التحكم للمصادقة.
    """
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.login_view = LoginView(self)
        self._connect_signals()

    def _connect_signals(self):
        """
        يربط إشارات الواجهة (مثل نقرات الأزرار) بالوظائف المناسبة.
        """
        self.login_view.login_button.clicked.connect(self.handle_login)

    def show_login(self):
        """
        يعرض واجهة تسجيل الدخول.
        """
        self.login_view.show()

    def handle_login(self):
        """
        يعالج منطق تسجيل الدخول عند الضغط على الزر.
        """
        email = self.login_view.email_input.text().strip()
        password = self.login_view.password_input.text()

        # التحقق الأساسي من المدخلات
        if not email or not password:
            self.login_view.error_label.setText("يرجى إدخال البريد الإلكتروني وكلمة المرور.")
            self.login_view.error_label.show()
            return

        # تغيير نص الزر للإشارة إلى أن العملية جارية
        self.login_view.login_button.setText("جارٍ تسجيل الدخول...")
        self.login_view.login_button.setEnabled(False)

        # استدعاء خدمة المصادقة
        user_data = self.firebase_service.sign_in_with_password(email, password)

        # إعادة الزر إلى حالته الأصلية
        self.login_view.login_button.setText("تسجيل الدخول")
        self.login_view.login_button.setEnabled(True)

        if user_data and 'idToken' in user_data:
            # نجاح تسجيل الدخول
            print("تم تسجيل الدخول بنجاح!", user_data)
            self.login_view.hide()
            # هنا سيتم لاحقًا عرض لوحة التحكم الرئيسية
            # self.main_dashboard = DashboardView()
            # self.main_dashboard.show()
        else:
            # فشل تسجيل الدخول
            error_message = "البريد الإلكتروني أو كلمة المرور غير صحيحة."
            # يمكنك إضافة معالجة أكثر تفصيلاً لرسائل الخطأ من Firebase هنا إذا أردت
            self.login_view.error_label.setText(error_message)
            self.login_view.error_label.show()
