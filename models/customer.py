class Customer:
    """
    Customer model class representing a customer with its properties.
    """
    
    def __init__(self, id: int, first_name: str, last_name: str, email: str, phone: str, address: str):
        """
        Initialize a Customer instance.
        
        Args:
            id (int): Unique identifier for the customer
            first_name (str): First name of the customer
            last_name (str): Last name of the customer
            email (str): Email address of the customer
            phone (str): Phone number of the customer
            address (str): Address of the customer
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
    
    def __repr__(self):
        """
        String representation of the Customer object.
        """
        return f"Customer(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', phone='{self.phone}', address='{self.address}')"
    
    def __str__(self):
        """
        Human-readable string representation of the Customer object.
        """
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def to_dict(self):
        """
        Convert the Customer object to a dictionary for JSON serialization.
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address
        }