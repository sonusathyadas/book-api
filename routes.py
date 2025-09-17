from flask import Blueprint, jsonify, request
from datetime import date
from models.book import Book

# Create Blueprint for book routes
book_bp = Blueprint('books', __name__, url_prefix='/api/books')

# Sample book data - minimum 5 books
books = [
    Book(1, "To Kill a Mockingbird", "Harper Lee", date(1960, 7, 11), "English", 281),
    Book(2, "1984", "George Orwell", date(1949, 6, 8), "English", 328),
    Book(3, "Pride and Prejudice", "Jane Austen", date(1813, 1, 28), "English", 432),
    Book(4, "The Great Gatsby", "F. Scott Fitzgerald", date(1925, 4, 10), "English", 180),
    Book(5, "One Hundred Years of Solitude", "Gabriel García Márquez", date(1967, 6, 5), "Spanish", 417),
    Book(6, "The Catcher in the Rye", "J.D. Salinger", date(1951, 7, 16), "English", 277),
    Book(7, "Lord of the Flies", "William Golding", date(1954, 9, 17), "English", 224)
]

def find_book_by_id(book_id):
    """Helper function to find a book by ID"""
    return next((book for book in books if book.id == book_id), None)

def get_next_id():
    """Helper function to get the next available ID"""
    return max([book.id for book in books], default=0) + 1

@book_bp.route('/', methods=['GET'])
def get_all_books():
    """Get all books"""
    return jsonify([book.to_dict() for book in books])

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """Get a book by its ID"""
    book = find_book_by_id(book_id)
    if book:
        return jsonify(book.to_dict())
    return jsonify({'error': 'Book not found'}), 404

@book_bp.route('/', methods=['POST'])
def create_book():
    """Create a new book"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'author', 'published_date', 'language', 'no_of_pages']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Parse the published_date
        try:
            published_date = date.fromisoformat(data['published_date'])
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Create new book
        new_book = Book(
            id=get_next_id(),
            title=data['title'],
            author=data['author'],
            published_date=published_date,
            language=data['language'],
            no_of_pages=int(data['no_of_pages'])
        )
        
        books.append(new_book)
        return jsonify(new_book.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update an existing book"""
    try:
        book = find_book_by_id(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'published_date' in data:
            try:
                book.published_date = date.fromisoformat(data['published_date'])
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        if 'language' in data:
            book.language = data['language']
        if 'no_of_pages' in data:
            book.no_of_pages = int(data['no_of_pages'])
        
        return jsonify(book.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book"""
    book = find_book_by_id(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    books.remove(book)
    return jsonify({'message': 'Book deleted successfully'}), 200

@book_bp.route('/search', methods=['GET'])
def search_book():
    """Search books by title, author, or language"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400
    
    # Search in title, author, and language
    matching_books = []
    for book in books:
        if (query in book.title.lower() or 
            query in book.author.lower() or 
            query in book.language.lower()):
            matching_books.append(book)
    
    return jsonify([book.to_dict() for book in matching_books])