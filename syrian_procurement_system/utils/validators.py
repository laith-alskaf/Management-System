# -*- coding: utf-8 -*-

"""
وحدة التحقق من صحة البيانات (Validators)
"""

import re

class ValidationResult:
    """
    تغلف نتيجة عملية التحقق.
    """
    def __init__(self, is_valid, message=None):
        self.is_valid = is_valid
        self.message = message

    def __bool__(self):
        return self.is_valid

def is_required(value, field_name):
    """
    يتحقق مما إذا كانت القيمة غير فارغة.
    """
    if not value or not value.strip():
        return ValidationResult(False, f"حقل '{field_name}' مطلوب.")
    return ValidationResult(True)

def is_numeric(value, field_name):
    """
    يتحقق مما إذا كانت القيمة رقمية (صحيحة أو عشرية).
    """
    if value:
        try:
            float(value)
        except (ValueError, TypeError):
            return ValidationResult(False, f"حقل '{field_name}' يجب أن يكون رقمًا.")
    return ValidationResult(True)

def is_integer(value, field_name):
    """
    يتحقق مما إذا كانت القيمة عددًا صحيحًا.
    """
    if value:
        try:
            int(value)
        except (ValueError, TypeError):
            return ValidationResult(False, f"حقل '{field_name}' يجب أن يكون عددًا صحيحًا.")
    return ValidationResult(True)

def is_email(value, field_name):
    """
    يتحقق من صحة تنسيق البريد الإلكتروني.
    """
    if value:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            return ValidationResult(False, f"حقل '{field_name}' يحتوي على بريد إلكتروني غير صالح.")
    return ValidationResult(True)

def run_validators(data, rules):
    """
    يشغل مجموعة من قواعد التحقق على البيانات ويعيد أول خطأ يتم العثور عليه.
    """
    for field, field_rules in rules.items():
        value = data.get(field)
        for validator, field_name in field_rules:
            result = validator(value, field_name)
            if not result:
                return result
    return ValidationResult(True)
