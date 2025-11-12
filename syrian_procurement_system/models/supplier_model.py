# -*- coding: utf-8 -*-

"""
نموذج البيانات الخاص بالموردين (Supplier Model)
"""

from sqlalchemy import Column, Integer, String
from services.local_db_service import Base

class Supplier(Base):
    """
    يمثل جدول الموردين في قاعدة البيانات.
    """
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    contact_person = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    address = Column(String, nullable=True)
    tax_number = Column(String, nullable=True, unique=True)
    rating = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Supplier(id={self.id}, name='{self.name}')>"
