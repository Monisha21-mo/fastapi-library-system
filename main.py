from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Library API Working"}
# Sample data
books = [
    {"id": 1, "title": "Python Basics", "author": "John", "available": True},
    {"id": 2, "title": "Data Science", "author": "Alice", "available": True},
    {"id": 3, "title": "AI Guide", "author": "Bob", "available": False}
]

@app.get("/books")
def get_books():
    return {
        "books": books,
        "total": len(books)
    }
class Book(BaseModel):
    title: str
    author: str
    available: bool
def filter_books(available: bool = None):
    result = books

    if available is not None:
        result = [b for b in result if b["available"] == available]

    return result

@app.get("/books/summary")
def get_summary():
    total = len(books)
    available = len([b for b in books if b["available"]])
    not_available = total - available

    return {
        "total_books": total,
        "available_books": available,
        "not_available_books": not_available
    }
@app.post("/books")
def add_book(book: Book):
    
    # Duplicate check
    for b in books:
        if b["title"].lower() == book.title.lower():
            return {"error": "Book already exists"}

    new_book = {
        "id": len(books) + 1,
        "title": book.title,
        "author": book.author,
        "available": book.available
    }

    books.append(new_book)

    return {
        "message": "Book added successfully",
        "book": new_book
    }
@app.get("/books/filter")
def filter_api(available: bool = None):

    filtered = filter_books(available)

    return {
        "filtered_books": filtered,
        "count": len(filtered)
    }
@app.get("/books/search")
def search_books(keyword: str):

    result = [
        b for b in books
        if keyword.lower() in b["title"].lower()
        or keyword.lower() in b["author"].lower()
    ]

    if not result:
        return {"message": "No books found"}

    return {
        "results": result,
        "count": len(result)
    }
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):

    for b in books:
        if b["id"] == book_id:
            b["title"] = book.title
            b["author"] = book.author
            b["available"] = book.available

            return {
                "message": "Book updated successfully",
                "book": b
            }

    return {"error": "Book not found"}
@app.get("/books/sort")
def sort_books(sort_by: str = "title", order: str = "asc"):

    reverse = True if order == "desc" else False

    sorted_books = sorted(books, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sorted_books": sorted_books
    }
@app.get("/books/page")
def paginate_books(page: int = 1, limit: int = 2):

    start = (page - 1) * limit
    end = start + limit

    total = len(books)
    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "data": books[start:end]
    }
@app.delete("/books/{book_id}")
def delete_book(book_id: int):

    for b in books:
        if b["id"] == book_id:
            books.remove(b)
            return {"message": "Book deleted successfully"}

    return {"error": "Book not found"}
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for b in books:
        if b["id"] == book_id:
            return b

    return {"error": "Book not found"}
@app.get("/books/sort")
def sort_books(sort_by: str = "title", order: str = "asc"):

    reverse = True if order == "desc" else False

    sorted_books = sorted(books, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sorted_books": sorted_books
    }
