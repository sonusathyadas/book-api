from datetime import date


class Book:
    """
    Book model class representing a book with its properties.
    """
    
    def __init__(self, id: int, title: str, author: str, published_date: date, language: str, no_of_pages: int):
        """
        Initialize a Book instance.
        
        Args:
            id (int): Unique identifier for the book
            title (str): Title of the book
            author (str): Author of the book
            published_date (date): Publication date of the book
            language (str): Language of the book
            no_of_pages (int): Number of pages in the book
        """
        self.id = id
        self.title = title
        self.author = author
        self.published_date = published_date
        self.language = language
        self.no_of_pages = no_of_pages
    
    def __repr__(self):
        """
        String representation of the Book object.
        """
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}', published_date={self.published_date}, language='{self.language}', no_of_pages={self.no_of_pages})"
    
    def __str__(self):
        """
        Human-readable string representation of the Book object.
        """
        return f"{self.title} by {self.author} ({self.published_date.year})"
    
    def to_dict(self):
        """
        Convert the Book object to a dictionary for JSON serialization.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'published_date': self.published_date.isoformat(),
            'language': self.language,
            'no_of_pages': self.no_of_pages
        }