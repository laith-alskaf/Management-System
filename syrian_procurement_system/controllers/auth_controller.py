# -*- coding: utf-8 -*-

"""
وحدة التحكم الخاصة بالمصادقة (Authentication Controller)
"""

from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QApplication
from services.firebase_service import FirebaseService
from views.auth_views.login_view import LoginView
from controllers.dashboard_controller import DashboardController
from utils.worker import Worker

class AuthController:
    """
    فئة وحدة التحكم للمصادقة.
    """
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.login_view = LoginView(self)
        self.dashboard_controller = None  # للحفاظ على مرجع لوحدة التحكم
        self.thread_pool = QThreadPool.globalInstance()
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
        يبدأ عملية تسجيل الدخول في خيط منفصل.
        """
        email = self.login_view.email_input.text().strip()
        password = self.login_view.password_input.text()

        if not email or not password:
            self._show_error("يرجى إدخال البريد الإلكتروني وكلمة المرور.")
            return

        self._set_loading_state(True)

        # إنشاء عامل لتشغيل مهمة تسجيل الدخول
        worker = Worker(self.firebase_service.sign_in_with_password, email, password)
        worker.signals.result.connect(self._on_login_result)
        worker.signals.error.connect(self._on_login_error)
        worker.signals.finished.connect(lambda: self._set_loading_state(False))

        self.thread_pool.start(worker)

    def _on_login_result(self, user_data):
        """
        يتم استدعاؤها عند نجاح عملية تسجيل الدخول.
        """
        if user_data and 'idToken' in user_data:
            print("تم تسجيل الدخول بنجاح!")
            self.login_view.close()
            self.dashboard_controller = DashboardController(logout_callback=self.show_login)
            self.dashboard_controller.show()
        else:
            # هذه الحالة قد تحدث إذا كانت الاستجابة غير متوقعة
            self._on_login_error()

    def _on_login_error(self, error_details=None):
        """
        يتم استدعاؤها عند فشل عملية تسجيل الدخول.
        """
        if error_details:
            print(f"Login Error: {error_details}")
        self._show_error("البريد الإلكتروني أو كلمة المرور غير صحيحة.")

    def _set_loading_state(self, is_loading):
        """
        تغيير حالة واجهة المستخدم لتعكس حالة التحميل.
        """
        if is_loading:
            self.login_view.error_label.hide()
            self.login_view.login_button.setText("جارٍ تسجيل الدخول...")
            self.login_view.login_button.setEnabled(False)
        else:
            self.login_view.login_button.setText("تسجيل الدخول")
            self.login_view.login_button.setEnabled(True)

        QApplication.processEvents()  # إجبار الواجهة على التحديث فوراً

    def _show_error(self, message):
        """
        يعرض رسالة خطأ في الواجهة.
        """
        self.login_view.error_label.setText(message)
        self.login_view.error_label.show()
