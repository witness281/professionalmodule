from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from decimal import Decimal

class BookBase(BaseModel):
    title: str
    author: str
    publisher_name: str
    rating: Optional[float] = 0.0
    price: Decimal
    stock: int
    is_electronic: bool = False
    publication_date: date
    description: Optional[str] = None
    genre_names: List[str] = []

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher_name: Optional[str] = None
    rating: Optional[float] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    is_electronic: Optional[bool] = None
    publication_date: Optional[date] = None
    description: Optional[str] = None
    genre_names: Optional[List[str]] = None

class BookResponse(BookBase):
    book_id: int
    image_path: Optional[str] = None
    
    class Config:
        from_attributes = True