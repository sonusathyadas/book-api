import pytest
import json
from datetime import date
from app import app
from models.book import Book
import routes


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Reset the books list to initial state for each test
            routes.books.clear()
            routes.books.extend([
                Book(1, "To Kill a Mockingbird", "Harper Lee", date(1960, 7, 11), "English", 281),
                Book(2, "1984", "George Orwell", date(1949, 6, 8), "English", 328),
                Book(3, "Pride and Prejudice", "Jane Austen", date(1813, 1, 28), "English", 432),
                Book(4, "The Great Gatsby", "F. Scott Fitzgerald", date(1925, 4, 10), "English", 180),
                Book(5, "One Hundred Years of Solitude", "Gabriel García Márquez", date(1967, 6, 5), "Spanish", 417),
                Book(6, "The Catcher in the Rye", "J.D. Salinger", date(1951, 7, 16), "English", 277),
                Book(7, "Lord of the Flies", "William Golding", date(1954, 9, 17), "English", 224)
            ])
            yield client


class TestGetAllBooks:
    """Test cases for GET /api/books endpoint."""
    
    def test_get_all_books_success(self, client):
        """Test successful retrieval of all books."""
        response = client.get('/api/books/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 7
        assert data[0]['title'] == "To Kill a Mockingbird"
        assert data[0]['author'] == "Harper Lee"
        assert data[1]['title'] == "1984"
        
    def test_get_all_books_returns_json(self, client):
        """Test that the response is valid JSON."""
        response = client.get('/api/books/')
        assert response.content_type == 'application/json'
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        for book in data:
            assert 'id' in book
            assert 'title' in book
            assert 'author' in book
            assert 'published_date' in book
            assert 'language' in book
            assert 'no_of_pages' in book


class TestGetBookById:
    """Test cases for GET /api/books/<id> endpoint."""
    
    def test_get_book_by_id_success(self, client):
        """Test successful retrieval of a book by ID."""
        response = client.get('/api/books/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['title'] == "To Kill a Mockingbird"
        assert data['author'] == "Harper Lee"
        assert data['published_date'] == "1960-07-11"
        assert data['language'] == "English"
        assert data['no_of_pages'] == 281
        
    def test_get_book_by_id_not_found(self, client):
        """Test retrieval of non-existent book."""
        response = client.get('/api/books/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['error'] == 'Book not found'
        
    def test_get_book_by_id_edge_cases(self, client):
        """Test edge cases for book ID."""
        # Test with ID 0
        response = client.get('/api/books/0')
        assert response.status_code == 404
        
        # Test with negative ID
        response = client.get('/api/books/-1')
        assert response.status_code == 404


class TestCreateBook:
    """Test cases for POST /api/books endpoint."""
    
    def test_create_book_success(self, client):
        """Test successful creation of a new book."""
        new_book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_date': '2023-01-01',
            'language': 'English',
            'no_of_pages': 300
        }
        
        response = client.post('/api/books/', 
                              data=json.dumps(new_book_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['title'] == 'Test Book'
        assert data['author'] == 'Test Author'
        assert data['published_date'] == '2023-01-01'
        assert data['language'] == 'English'
        assert data['no_of_pages'] == 300
        assert data['id'] == 8  # Next available ID
        
    def test_create_book_missing_required_fields(self, client):
        """Test creation with missing required fields."""
        required_fields = ['title', 'author', 'published_date', 'language', 'no_of_pages']
        
        for field in required_fields:
            incomplete_data = {
                'title': 'Test Book',
                'author': 'Test Author',
                'published_date': '2023-01-01',
                'language': 'English',
                'no_of_pages': 300
            }
            del incomplete_data[field]
            
            response = client.post('/api/books/',
                                  data=json.dumps(incomplete_data),
                                  content_type='application/json')
            assert response.status_code == 400
            
            data = json.loads(response.data)
            assert f'Missing required field: {field}' in data['error']
            
    def test_create_book_invalid_date_format(self, client):
        """Test creation with invalid date format."""
        new_book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_date': 'invalid-date',
            'language': 'English',
            'no_of_pages': 300
        }
        
        response = client.post('/api/books/',
                              data=json.dumps(new_book_data),
                              content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'Invalid date format' in data['error']
        
    def test_create_book_invalid_pages_format(self, client):
        """Test creation with invalid no_of_pages format."""
        new_book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_date': '2023-01-01',
            'language': 'English',
            'no_of_pages': 'not-a-number'
        }
        
        response = client.post('/api/books/',
                              data=json.dumps(new_book_data),
                              content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_create_book_no_json_data(self, client):
        """Test creation without JSON data."""
        response = client.post('/api/books/')
        assert response.status_code == 400


class TestUpdateBook:
    """Test cases for PUT /api/books/<id> endpoint."""
    
    def test_update_book_success(self, client):
        """Test successful update of an existing book."""
        update_data = {
            'title': 'Updated Title',
            'author': 'Updated Author'
        }
        
        response = client.put('/api/books/1',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['title'] == 'Updated Title'
        assert data['author'] == 'Updated Author'
        # Other fields should remain unchanged
        assert data['published_date'] == "1960-07-11"
        assert data['language'] == "English"
        assert data['no_of_pages'] == 281
        
    def test_update_book_all_fields(self, client):
        """Test updating all fields of a book."""
        update_data = {
            'title': 'Completely New Title',
            'author': 'New Author',
            'published_date': '2024-01-01',
            'language': 'Spanish',
            'no_of_pages': 500
        }
        
        response = client.put('/api/books/2',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['id'] == 2
        assert data['title'] == 'Completely New Title'
        assert data['author'] == 'New Author'
        assert data['published_date'] == '2024-01-01'
        assert data['language'] == 'Spanish'
        assert data['no_of_pages'] == 500
        
    def test_update_book_not_found(self, client):
        """Test updating non-existent book."""
        update_data = {'title': 'New Title'}
        
        response = client.put('/api/books/999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['error'] == 'Book not found'
        
    def test_update_book_invalid_date(self, client):
        """Test updating with invalid date format."""
        update_data = {'published_date': 'invalid-date'}
        
        response = client.put('/api/books/1',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'Invalid date format' in data['error']
        
    def test_update_book_empty_data(self, client):
        """Test updating with empty data (should work)."""
        response = client.put('/api/books/1',
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 200
        
        # Book should remain unchanged
        data = json.loads(response.data)
        assert data['title'] == "To Kill a Mockingbird"


class TestDeleteBook:
    """Test cases for DELETE /api/books/<id> endpoint."""
    
    def test_delete_book_success(self, client):
        """Test successful deletion of a book."""
        # Verify book exists first
        response = client.get('/api/books/1')
        assert response.status_code == 200
        
        # Delete the book
        response = client.delete('/api/books/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['message'] == 'Book deleted successfully'
        
        # Verify book is deleted
        response = client.get('/api/books/1')
        assert response.status_code == 404
        
        # Verify total count decreased
        response = client.get('/api/books/')
        data = json.loads(response.data)
        assert len(data) == 6  # Should be 6 instead of 7
        
    def test_delete_book_not_found(self, client):
        """Test deletion of non-existent book."""
        response = client.delete('/api/books/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['error'] == 'Book not found'
        
    def test_delete_book_multiple_deletions(self, client):
        """Test deleting multiple books."""
        # Delete book 1
        response = client.delete('/api/books/1')
        assert response.status_code == 200
        
        # Delete book 2
        response = client.delete('/api/books/2')
        assert response.status_code == 200
        
        # Verify both are deleted
        response = client.get('/api/books/')
        data = json.loads(response.data)
        assert len(data) == 5
        
        # Verify correct books remain
        remaining_ids = [book['id'] for book in data]
        assert 1 not in remaining_ids
        assert 2 not in remaining_ids
        assert 3 in remaining_ids


class TestSearchBooks:
    """Test cases for GET /api/books/search endpoint."""
    
    def test_search_books_by_title(self, client):
        """Test searching books by title."""
        response = client.get('/api/books/search?q=1984')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['title'] == '1984'
        assert data[0]['author'] == 'George Orwell'
        
    def test_search_books_by_author(self, client):
        """Test searching books by author."""
        response = client.get('/api/books/search?q=Harper Lee')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['title'] == 'To Kill a Mockingbird'
        assert data[0]['author'] == 'Harper Lee'
        
    def test_search_books_by_language(self, client):
        """Test searching books by language."""
        response = client.get('/api/books/search?q=Spanish')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['title'] == 'One Hundred Years of Solitude'
        assert data[0]['language'] == 'Spanish'
        
    def test_search_books_case_insensitive(self, client):
        """Test that search is case insensitive."""
        response = client.get('/api/books/search?q=harper lee')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['author'] == 'Harper Lee'
        
        response = client.get('/api/books/search?q=ENGLISH')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 6  # All books except the Spanish one
        
    def test_search_books_partial_match(self, client):
        """Test searching with partial matches."""
        response = client.get('/api/books/search?q=Pride')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['title'] == 'Pride and Prejudice'
        
    def test_search_books_no_results(self, client):
        """Test searching with no matching results."""
        response = client.get('/api/books/search?q=nonexistent')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 0
        assert data == []
        
    def test_search_books_missing_query(self, client):
        """Test searching without query parameter."""
        response = client.get('/api/books/search')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['error'] == 'Query parameter "q" is required'
        
    def test_search_books_empty_query(self, client):
        """Test searching with empty query parameter."""
        response = client.get('/api/books/search?q=')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['error'] == 'Query parameter "q" is required'
        
    def test_search_books_multiple_matches(self, client):
        """Test searching with query that matches multiple books."""
        response = client.get('/api/books/search?q=the')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) >= 2  # Should match multiple books with "the" in title
        
        titles = [book['title'] for book in data]
        assert 'The Great Gatsby' in titles
        assert 'The Catcher in the Rye' in titles


class TestHelperFunctions:
    """Test cases for helper functions."""
    
    def test_find_book_by_id(self, client):
        """Test the find_book_by_id helper function."""
        # This is tested indirectly through the API endpoints
        # but we can test it directly if needed
        book = routes.find_book_by_id(1)
        assert book is not None
        assert book.title == "To Kill a Mockingbird"
        
        book = routes.find_book_by_id(999)
        assert book is None
        
    def test_get_next_id(self, client):
        """Test the get_next_id helper function."""
        next_id = routes.get_next_id()
        assert next_id == 8  # Should be max(7) + 1
        
        # Add a book and test again
        new_book = Book(10, "Test", "Author", date.today(), "English", 100)
        routes.books.append(new_book)
        
        next_id = routes.get_next_id()
        assert next_id == 11  # Should be max(10) + 1


class TestIntegrationScenarios:
    """Integration test scenarios combining multiple operations."""
    
    def test_create_update_delete_flow(self, client):
        """Test complete CRUD flow for a book."""
        # Create a new book
        new_book_data = {
            'title': 'Integration Test Book',
            'author': 'Test Author',
            'published_date': '2023-01-01',
            'language': 'English',
            'no_of_pages': 250
        }
        
        response = client.post('/api/books/',
                              data=json.dumps(new_book_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        created_book = json.loads(response.data)
        book_id = created_book['id']
        
        # Update the book
        update_data = {'title': 'Updated Integration Test Book'}
        response = client.put(f'/api/books/{book_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        updated_book = json.loads(response.data)
        assert updated_book['title'] == 'Updated Integration Test Book'
        
        # Search for the book
        response = client.get('/api/books/search?q=Updated Integration')
        assert response.status_code == 200
        
        search_results = json.loads(response.data)
        assert len(search_results) == 1
        assert search_results[0]['id'] == book_id
        
        # Delete the book
        response = client.delete(f'/api/books/{book_id}')
        assert response.status_code == 200
        
        # Verify it's deleted
        response = client.get(f'/api/books/{book_id}')
        assert response.status_code == 404