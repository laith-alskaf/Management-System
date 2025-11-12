# -*- coding: utf-8 -*-

"""
نموذج البيانات الخاص بالموردين (Supplier Model)
"""

from sqlalchemy import Column, Integer, String
from syrian_procurement_system.services.local_db_service import Base

class Supplier(Base):
    """
    فئة تمثل جدول الموردين في قاعدة البيانات.
    """
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    contact_person = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)

    def __repr__(self):
        return f"<Supplier(id={self.id}, name='{self.name}')>"
