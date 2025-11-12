# -*- coding: utf-8 -*-

"""
خدمات قاعدة البيانات المحلية SQLite
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# تحديد مسار قاعدة البيانات في المجلد الرئيسي للمشروع
DATABASE_URL = "sqlite:///syrian_procurement_system.db"

# إنشاء محرك قاعدة البيانات
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# إنشاء جلسة (Session) للتعامل مع قاعدة البيانات
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# إنشاء الفئة الأساسية للنماذج (Models)
Base = declarative_base()

def init_db():
    """
    تقوم بإنشاء جميع الجداول في قاعدة البيانات.
    يتم استدعاؤها مرة واحدة عند بدء تشغيل التطبيق.
    """
    # استيراد النماذج هنا لضمان تسجيلها مع Base
    from models.supplier_model import Supplier
    Base.metadata.create_all(bind=engine)

class LocalDbService:
    """
    فئة لتغليف التفاعلات مع قاعدة البيانات المحلية.
    """
    def __init__(self):
        """
        يقوم بتهيئة جلسة جديدة لقاعدة البيانات.
        """
        self.db = SessionLocal()

    def get_db(self):
        """
        تُرجع كائن الجلسة.
        """
        return self.db

    def close(self):
        """
        تغلق جلسة قاعدة البيانات.
        """
        self.db.close()

    # --- CRUD Operations for Suppliers ---

    def add_supplier(self, name, contact_person, phone, email, address):
        """
        يضيف موردًا جديدًا إلى قاعدة البيانات.
        """
        from models.supplier_model import Supplier
        new_supplier = Supplier(
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address
        )
        self.db.add(new_supplier)
        self.db.commit()
        self.db.refresh(new_supplier)
        return new_supplier

    def get_all_suppliers(self):
        """
        يسترجع جميع الموردين من قاعدة البيانات.
        """
        from models.supplier_model import Supplier
        return self.db.query(Supplier).all()

    def get_supplier_by_id(self, supplier_id):
        """
        يسترجع موردًا محددًا بواسطة معرفه.
        """
        from models.supplier_model import Supplier
        return self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

    def update_supplier(self, supplier_id, name, contact_person, phone, email, address):
        """
        يحدّث بيانات مورد موجود.
        """
        supplier = self.get_supplier_by_id(supplier_id)
        if supplier:
            supplier.name = name
            supplier.contact_person = contact_person
            supplier.phone = phone
            supplier.email = email
            supplier.address = address
            self.db.commit()
            return supplier
        return None

    def delete_supplier(self, supplier_id):
        """
        يحذف موردًا من قاعدة البيانات.
        """
        from models.supplier_model import Supplier
        supplier = self.db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if supplier:
            self.db.delete(supplier)
            self.db.commit()
            return True
        return False
