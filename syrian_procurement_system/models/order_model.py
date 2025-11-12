# -*- coding: utf-8 -*-

"""
نماذج البيانات الخاصة بأوامر الشراء (Order Models)
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from services.local_db_service import Base
import datetime

class Order(Base):
    """
    يمثل جدول أوامر الشراء الرئيسي.
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date, nullable=False, default=datetime.date.today)
    status = Column(Enum('قيد الانتظار', 'معالجة', 'مكتمل', 'ملغى', name='order_status_enum'),
                    nullable=False, default='قيد الانتظار')

    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    supplier = relationship("Supplier")

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, status='{self.status}')>"

class OrderItem(Base):
    """
    يمثل المواد الموجودة داخل أمر شراء معين.
    """
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    price_at_time_of_order = Column(Float, nullable=False)

    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    order = relationship("Order", back_populates="items")

    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    material = relationship("Material")

    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, material_id={self.material_id}, quantity={self.quantity})>"
