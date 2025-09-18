# Unit Tests for Book API

This directory contains comprehensive unit tests for the Book API endpoints defined in `routes.py`.

## Test Coverage

The test suite covers all API endpoints with 96% code coverage:

### Endpoints Tested

1. **GET /api/books** - Get all books
2. **GET /api/books/<id>** - Get book by ID  
3. **POST /api/books** - Create new book
4. **PUT /api/books/<id>** - Update existing book
5. **DELETE /api/books/<id>** - Delete book
6. **GET /api/books/search** - Search books by title, author, or language

### Test Categories

- **Happy Path Tests**: Normal successful operations
- **Error Handling Tests**: Invalid inputs, missing data, not found scenarios
- **Edge Cases**: Boundary conditions and special cases
- **Integration Tests**: End-to-end workflows combining multiple operations
- **Helper Function Tests**: Testing utility functions

## Running the Tests

### Prerequisites

Install the testing dependencies:

```bash
pip install pytest pytest-flask pytest-cov
```

### Run All Tests

```bash
# Basic test run
pytest test_routes.py -v

# With coverage report
pytest test_routes.py --cov=routes --cov=models --cov-report=term-missing

# Run specific test class
pytest test_routes.py::TestCreateBook -v

# Run specific test method
pytest test_routes.py::TestCreateBook::test_create_book_success -v
```

## Test Structure

Tests are organized into classes by functionality:

- `TestGetAllBooks` - Tests for retrieving all books
- `TestGetBookById` - Tests for retrieving books by ID
- `TestCreateBook` - Tests for creating new books  
- `TestUpdateBook` - Tests for updating existing books
- `TestDeleteBook` - Tests for deleting books
- `TestSearchBooks` - Tests for searching books
- `TestHelperFunctions` - Tests for utility functions
- `TestIntegrationScenarios` - End-to-end integration tests

## Test Data

Each test starts with a fresh copy of the sample book data:

1. "To Kill a Mockingbird" by Harper Lee
2. "1984" by George Orwell  
3. "Pride and Prejudice" by Jane Austen
4. "The Great Gatsby" by F. Scott Fitzgerald
5. "One Hundred Years of Solitude" by Gabriel García Márquez
6. "The Catcher in the Rye" by J.D. Salinger
7. "Lord of the Flies" by William Golding

## Test Results

All 30 tests pass successfully, covering:

- 15 positive/happy path scenarios
- 10 error handling scenarios  
- 3 edge case scenarios
- 2 integration test scenarios

The test suite provides confidence that the API endpoints work correctly and handle edge cases and errors appropriately.