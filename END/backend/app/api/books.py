from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date, datetime, timedelta
import os
import shutil
from PIL import Image

from backend.app.core.database import get_db
from backend.app.core.config import settings
from backend.app.models.book import Book, Publisher, Genre
from backend.app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.utils.image_handler import save_book_image, validate_image

router = APIRouter(prefix="/api/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
def get_books(
    search: Optional[str] = None,
    genre: Optional[str] = None,
    in_stock: Optional[bool] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    
    if search:
        query = query.filter(
            Book.title.ilike(f"%{search}%") | 
            Book.description.ilike(f"%{search}%")
        )
    
    if genre:
        query = query.join(Book.genres).filter(Genre.genre_name == genre)
    
    if in_stock:
        query = query.filter(Book.stock > 0)
    
    if sort_by == "publication_date":
        if sort_order == "desc":
            query = query.order_by(Book.publication_date.desc())
        else:
            query = query.order_by(Book.publication_date.asc())
    else:
        query = query.order_by(Book.book_id)
    
    books = query.all()
    
    result = []
    for book in books:
        book_data = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "publisher_name": book.publisher.publisher_name if book.publisher else None,
            "rating": book.rating,
            "price": book.price,
            "stock": book.stock,
            "is_electronic": book.is_electronic,
            "publication_date": book.publication_date,
            "description": book.description,
            "image_path": book.image_path,
            "genre_names": [g.genre_name for g in book.genres]
        }
        result.append(BookResponse(**book_data))
    
    return result

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return BookResponse(
        book_id=book.book_id,
        title=book.title,
        author=book.author,
        publisher_name=book.publisher.publisher_name if book.publisher else None,
        rating=book.rating,
        price=book.price,
        stock=book.stock,
        is_electronic=book.is_electronic,
        publication_date=book.publication_date,
        description=book.description,
        image_path=book.image_path,
        genre_names=[g.genre_name for g in book.genres]
    )

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    title: str,
    author: str,
    publisher_name: str,
    price: float,
    stock: int,
    publication_date: date,
    rating: Optional[float] = 0.0,
    is_electronic: bool = False,
    description: Optional[str] = None,
    genre_names: str = "",
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if price < 0 or stock < 0:
        raise HTTPException(status_code=400, detail="Price and stock cannot be negative")
    
    publisher = db.query(Publisher).filter(Publisher.publisher_name == publisher_name).first()
    if not publisher:
        publisher = Publisher(publisher_name=publisher_name)
        db.add(publisher)
        db.flush()
    
    image_path = None
    if image:
        validate_image(image)
        image_path = save_book_image(image)
    
    book = Book(
        title=title,
        author=author,
        publisher_id=publisher.publisher_id,
        rating=rating,
        price=price,
        stock=stock,
        is_electronic=is_electronic,
        publication_date=publication_date,
        description=description,
        image_path=image_path
    )
    
    db.add(book)
    db.flush()
    
    if genre_names:
        genre_list = [g.strip() for g in genre_names.split(",")]
        for genre_name in genre_list:
            genre = db.query(Genre).filter(Genre.genre_name == genre_name).first()
            if not genre:
                genre = Genre(genre_name=genre_name)
                db.add(genre)
                db.flush()
            book.genres.append(genre)
    
    db.commit()
    db.refresh(book)
    
    return BookResponse(
        book_id=book.book_id,
        title=book.title,
        author=book.author,
        publisher_name=publisher.publisher_name,
        rating=book.rating,
        price=book.price,
        stock=book.stock,
        is_electronic=book.is_electronic,
        publication_date=book.publication_date,
        description=book.description,
        image_path=book.image_path,
        genre_names=[g.genre_name for g in book.genres]
    )

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book_update.title is not None:
        book.title = book_update.title
    if book_update.author is not None:
        book.author = book_update.author
    if book_update.publisher_name is not None:
        publisher = db.query(Publisher).filter(Publisher.publisher_name == book_update.publisher_name).first()
        if not publisher:
            publisher = Publisher(publisher_name=book_update.publisher_name)
            db.add(publisher)
            db.flush()
        book.publisher_id = publisher.publisher_id
    if book_update.rating is not None:
        book.rating = book_update.rating
    if book_update.price is not None:
        if book_update.price < 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative")
        book.price = book_update.price
    if book_update.stock is not None:
        if book_update.stock < 0:
            raise HTTPException(status_code=400, detail="Stock cannot be negative")
        book.stock = book_update.stock
    if book_update.is_electronic is not None:
        book.is_electronic = book_update.is_electronic
    if book_update.publication_date is not None:
        book.publication_date = book_update.publication_date
    if book_update.description is not None:
        book.description = book_update.description
    
    if book_update.genre_names is not None:
        book.genres = []
        for genre_name in book_update.genre_names:
            genre = db.query(Genre).filter(Genre.genre_name == genre_name).first()
            if not genre:
                genre = Genre(genre_name=genre_name)
                db.add(genre)
                db.flush()
            book.genres.append(genre)
    
    db.commit()
    db.refresh(book)
    
    return BookResponse(
        book_id=book.book_id,
        title=book.title,
        author=book.author,
        publisher_name=book.publisher.publisher_name if book.publisher else None,
        rating=book.rating,
        price=book.price,
        stock=book.stock,
        is_electronic=book.is_electronic,
        publication_date=book.publication_date,
        description=book.description,
        image_path=book.image_path,
        genre_names=[g.genre_name for g in book.genres]
    )

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.order_items:
        raise HTTPException(status_code=400, detail="Cannot delete book that has orders")
    
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}