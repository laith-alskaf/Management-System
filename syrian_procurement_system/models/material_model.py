# -*- coding: utf-8 -*-

"""
نموذج البيانات الخاص بالمواد والمستلزمات (Material Model)
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from services.local_db_service import Base

class Material(Base):
    """
    يمثل جدول المواد في قاعدة البيانات.
    """
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False, default=0.0)
    expiry_date = Column(Date, nullable=True)
    barcode = Column(String, nullable=True, unique=True)

    # يمكن إضافة علاقة مع الموردين لاحقاً إذا أردنا معرفة من أي مورد تم شراء المادة
    # supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    # supplier = relationship("Supplier")

    def __repr__(self):
        return f"<Material(id={self.id}, name='{self.name}')>"
