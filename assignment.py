from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

# Initialize FastAPI with project metadata
app = FastAPI(
    title="Bookstore API",
    description="A simple API to manage a bookstore inventory",
    version="1.0.0",
)

# In-memory "database" (Updated with Exercise 3: category field)
books_db = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 12.99, "stock": 10, "release_date": None, "category": "Fiction"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 14.99, "stock": 5, "release_date": None, "category": "Fiction"},
    {"id": 3, "title": "1984", "author": "George Orwell", "price": 9.99, "stock": 15, "release_date": None, "category": "Fiction"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "price": 11.99, "stock": 7, "release_date": None, "category": "Romance"},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "price": 10.99, "stock": 8, "release_date": None, "category": "Fiction"},
]

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, le=10000)
    stock: int = Field(..., ge=0, le=1000)
    release_date: Optional[datetime] = Field(None, description="The publication date of the book")
    # Exercise 3: Added required category field
    category: str = Field(..., min_length=1, max_length=50, description="Genre or category of the book")

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0, le=10000)
    stock: Optional[int] = Field(None, ge=0, le=1000)
    release_date: Optional[datetime] = Field(None, description="The publication date of the book")
    # Exercise 3: Added optional category field for partial updates
    category: Optional[str] = Field(None, min_length=1, max_length=50, description="Genre or category of the book")

@app.get("/books")
def get_books(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0, le=100)):
    return books_db[skip : skip + limit]

# 2. Search for books by title or author (MUST BE ABOVE THE ID ROUTE!)
@app.get("/books/search")
def search_books(q: str, author: Optional[str] = None):
    results = []
    for book in books_db:
        if q.lower() in book["title"].lower() or q.lower() in book["author"].lower():
            if author:
                if author.lower() in book["author"].lower():
                    results.append(book)
            else:
                results.append(book)
    return results

# 3. Retrieve a single book by its path parameter ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books")
def add_book(book: BookCreate):
    for existing_book in books_db:
        if (existing_book["title"].lower() == book.title.lower() and 
            existing_book["author"].lower() == book.author.lower()):
            raise HTTPException(status_code=400, detail="Book already exists")
            
    new_id = max([b["id"] for b in books_db]) + 1 if books_db else 1
    
    new_book = {
        "id": new_id,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "stock": book.stock,
        "release_date": book.release_date,
        "category": book.category  # Exercise 3: Capture the category field
    }
    
    books_db.append(new_book)
    return {"message": "Book added successfully", "book": new_book}
@app.put("/books/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            if book_update.title is not None:
                books_db[index]["title"] = book_update.title
            if book_update.author is not None:
                books_db[index]["author"] = book_update.author
            if book_update.price is not None:
                books_db[index]["price"] = book_update.price
            if book_update.stock is not None:
                books_db[index]["stock"] = book_update.stock
            if book_update.release_date is not None:
                books_db[index]["release_date"] = book_update.release_date
            # Exercise 3: Allow partial updates to the category field
            if book_update.category is not None:
                books_db[index]["category"] = book_update.category
                
            return {"message": "Book updated successfully", "book": books_db[index]}
            
    raise HTTPException(status_code=404, detail="Book not found")
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            deleted_book = books_db.pop(index)
            return {"message": "Book deleted successfully", "book": deleted_book}
            
    raise HTTPException(status_code=404, detail="Book not found")