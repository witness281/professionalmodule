from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.core.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.user_id"))
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    delivery_date = Column(Date)
    status = Column(String(20), nullable=False, default="Новый")
    
    customer = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    order_id = Column(Integer, ForeignKey("orders.order_id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.book_id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price_at_time = Column(DECIMAL(10, 2), nullable=False)
    
    order = relationship("Order", back_populates="order_items")
    book = relationship("Book", back_populates="order_items")