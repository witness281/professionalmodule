from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal

from app.core.database import get_db
from app.models.order import Order, OrderItem
from app.models.book import Book
from app.models.user import User
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderItemResponse

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.get("/", response_model=List[OrderResponse])
def get_orders(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.all()
    return [
        OrderResponse(
            order_id=o.order_id,
            customer_name=o.customer.full_name,
            order_date=o.order_date,
            delivery_date=o.delivery_date,
            status=o.status,
            items=[
                OrderItemResponse(
                    book_title=item.book.title,
                    quantity=item.quantity,
                    price_at_time=item.price_at_time
                )
                for item in o.order_items
            ]
        )
        for o in orders
    ]

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return OrderResponse(
        order_id=order.order_id,
        customer_name=order.customer.full_name,
        order_date=order.order_date,
        delivery_date=order.delivery_date,
        status=order.status,
        items=[
            OrderItemResponse(
                book_title=item.book.title,
                quantity=item.quantity,
                price_at_time=item.price_at_time
            )
            for item in order.order_items
        ]
    )

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    customer = db.query(User).filter(User.user_id == order_data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    total = Decimal(0)
    order_items = []
    
    for item in order_data.items:
        book = db.query(Book).filter(Book.book_id == item.book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail=f"Book {item.book_id} not found")
        if book.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {book.title}")
        
        book.stock -= item.quantity
        order_items.append({
            "book_id": item.book_id,
            "quantity": item.quantity,
            "price_at_time": book.price
        })
        total += book.price * item.quantity
    
    order = Order(
        customer_id=order_data.customer_id,
        delivery_date=order_data.delivery_date,
        status="Новый"
    )
    db.add(order)
    db.flush()
    
    for item_data in order_items:
        order_item = OrderItem(
            order_id=order.order_id,
            book_id=item_data["book_id"],
            quantity=item_data["quantity"],
            price_at_time=item_data["price_at_time"]
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    
    return OrderResponse(
        order_id=order.order_id,
        customer_name=customer.full_name,
        order_date=order.order_date,
        delivery_date=order.delivery_date,
        status=order.status,
        items=[
            OrderItemResponse(
                book_title=db.query(Book).filter(Book.book_id == item.book_id).first().title,
                quantity=item.quantity,
                price_at_time=item.price_at_time
            )
            for item in order.order_items
        ]
    )

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order_update.delivery_date is not None:
        order.delivery_date = order_update.delivery_date
    if order_update.status is not None:
        order.status = order_update.status
    
    db.commit()
    db.refresh(order)
    
    return OrderResponse(
        order_id=order.order_id,
        customer_name=order.customer.full_name,
        order_date=order.order_date,
        delivery_date=order.delivery_date,
        status=order.status,
        items=[
            OrderItemResponse(
                book_title=item.book.title,
                quantity=item.quantity,
                price_at_time=item.price_at_time
            )
            for item in order.order_items
        ]
    )