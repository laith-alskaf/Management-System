# -*- coding: utf-8 -*-

"""
خدمات Firebase للمصادقة وإدارة البيانات
"""

import requests
import json
from syrian_procurement_system.config.firebase_config import FIREBASE_CONFIG

class FirebaseService:
    """
    فئة لتغليف التفاعلات مع خدمات Firebase.
    """
    def __init__(self):
        """
        يقوم بتهيئة الخدمة مع مفتاح API الخاص بـ Firebase.
        """
        self.api_key = FIREBASE_CONFIG.get('apiKey')
        self.auth_base_url = "https://identitytoolkit.googleapis.com/v1/accounts"

    def sign_in_with_password(self, email, password):
        """
        تسجيل دخول المستخدم باستخدام البريد الإلكتروني وكلمة المرور.

        Args:
            email (str): البريد الإلكتر الإلكتروني للمستخدم.
            password (str): كلمة المرور للمستخدم.

        Returns:
            dict or None: بيانات المستخدم عند النجاح، أو None عند الفشل.
        """
        signin_url = f"{self.auth_base_url}:signInWithPassword?key={self.api_key}"

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        try:
            response = requests.post(signin_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
            response.raise_for_status()  # يثير استثناء لأكواد الحالة 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            # يمكنك هنا تسجيل الخطأ أو معالجته بشكل أفضل
            print(f"حدث خطأ أثناء الاتصال بـ Firebase: {e}")
            if e.response:
                print(f"تفاصيل الخطأ: {e.response.json()}")
            return None

# مثال للاستخدام (سيتم إزالته لاحقًا)
if __name__ == '__main__':
    # لا يمكن تشغيل هذا المثال بنجاح بدون مفتاح API حقيقي وحساب مستخدم
    firebase_service = FirebaseService()
    print("يرجى ملاحظة: هذا المثال لن يعمل بدون إعدادات Firebase صالحة ومستخدم مسجل.")
    # user_data = firebase_service.sign_in_with_password("test@example.com", "password123")
    # if user_data:
    #     print("تم تسجيل الدخول بنجاح:")
    #     print(user_data)
    # else:
    #     print("فشل تسجيل الدخول.")
