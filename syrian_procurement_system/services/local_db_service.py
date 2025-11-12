# -*- coding: utf-8 -*-

"""
خدمات قاعدة البيانات المحلية SQLite
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ... (الكود الخاص بإعداد قاعدة البيانات يبقى كما هو)
DATABASE_URL = "sqlite:///syrian_procurement_system.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from models.supplier_model import Supplier
    from models.material_model import Material
    from models.order_model import Order, OrderItem
    Base.metadata.create_all(bind=engine)

class LocalDbService:
    """
    فئة لتغليف التفاعلات مع قاعدة البيانات المحلية بشكل آمن للخيوط.
    جميع الدوال ثابتة (static) وتدير جلستها الخاصة.
    """

    @staticmethod
    def add_supplier(name, contact_person, phone, email, address):
        from models.supplier_model import Supplier
        with SessionLocal() as db:
            new_supplier = Supplier(name=name, contact_person=contact_person, phone=phone, email=email, address=address)
            db.add(new_supplier)
            db.commit()
            db.refresh(new_supplier)
            return new_supplier

    @staticmethod
    def get_all_suppliers():
        from models.supplier_model import Supplier
        with SessionLocal() as db:
            return db.query(Supplier).all()

    @staticmethod
    def get_supplier_by_id(supplier_id):
        from models.supplier_model import Supplier
        with SessionLocal() as db:
            return db.query(Supplier).filter(Supplier.id == supplier_id).first()

    @staticmethod
    def update_supplier(supplier_id, name, contact_person, phone, email, address):
        from models.supplier_model import Supplier
        with SessionLocal() as db:
            supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
            if supplier:
                supplier.name = name
                supplier.contact_person = contact_person
                supplier.phone = phone
                supplier.email = email
                supplier.address = address
                db.commit()
            return supplier

    @staticmethod
    def delete_supplier(supplier_id):
        from models.supplier_model import Supplier
        with SessionLocal() as db:
            supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
            if supplier:
                db.delete(supplier)
                db.commit()
                return True
            return False

    @staticmethod
    def add_material(name, category, quantity, price, expiry_date):
        from models.material_model import Material
        with SessionLocal() as db:
            new_material = Material(name=name, category=category, quantity=quantity, price=price, expiry_date=expiry_date)
            db.add(new_material)
            db.commit()
            db.refresh(new_material)
            return new_material

    @staticmethod
    def get_all_materials():
        from models.material_model import Material
        with SessionLocal() as db:
            return db.query(Material).all()

    @staticmethod
    def get_material_by_id(material_id):
        from models.material_model import Material
        with SessionLocal() as db:
            return db.query(Material).filter(Material.id == material_id).first()

    @staticmethod
    def update_material(material_id, name, category, quantity, price, expiry_date):
        from models.material_model import Material
        with SessionLocal() as db:
            material = db.query(Material).filter(Material.id == material_id).first()
            if material:
                material.name = name
                material.category = category
                material.quantity = quantity
                material.price = price
                material.expiry_date = expiry_date
                db.commit()
            return material

    @staticmethod
    def delete_material(material_id):
        from models.material_model import Material
        with SessionLocal() as db:
            material = db.query(Material).filter(Material.id == material_id).first()
            if material:
                db.delete(material)
                db.commit()
                return True
            return False
