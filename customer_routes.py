from flask import Blueprint, jsonify, request
from models.customer import Customer

# Create Blueprint for customer routes
customer_bp = Blueprint('customers', __name__, url_prefix='/api/customers')

# Sample customer data - in memory storage
customers = [
    Customer(1, "John", "Doe", "john.doe@email.com", "555-0101", "123 Main St, Anytown, USA", "MEM001"),
    Customer(2, "Jane", "Smith", "jane.smith@email.com", "555-0102", "456 Oak Ave, Somewhere, USA", "MEM002"),
    Customer(3, "Bob", "Johnson", "bob.johnson@email.com", "555-0103", "789 Pine Rd, Anywhere, USA", "MEM003"),
    Customer(4, "Alice", "Williams", "alice.williams@email.com", "555-0104", "321 Elm St, Nowhere, USA", "MEM004"),
    Customer(5, "Charlie", "Brown", "charlie.brown@email.com", "555-0105", "654 Maple Dr, Everywhere, USA", "MEM005")
]

def find_customer_by_id(customer_id):
    """Helper function to find a customer by ID"""
    return next((customer for customer in customers if customer.id == customer_id), None)

def get_next_customer_id():
    """Helper function to get the next available ID"""
    return max([customer.id for customer in customers], default=0) + 1

@customer_bp.route('/', methods=['GET'])
def get_all_customers():
    """Get all customers"""
    return jsonify([customer.to_dict() for customer in customers])

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    """Get a customer by its ID"""
    customer = find_customer_by_id(customer_id)
    if customer:
        return jsonify(customer.to_dict())
    return jsonify({'error': 'Customer not found'}), 404

@customer_bp.route('/', methods=['POST'])
def add_customer():
    """Create a new customer"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new customer
        new_customer = Customer(
            id=get_next_customer_id(),
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            membership_id=data.get('membership_id')
        )
        
        customers.append(new_customer)
        return jsonify(new_customer.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update an existing customer"""
    try:
        customer = find_customer_by_id(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'first_name' in data:
            customer.first_name = data['first_name']
        if 'last_name' in data:
            customer.last_name = data['last_name']
        if 'email' in data:
            customer.email = data['email']
        if 'phone' in data:
            customer.phone = data['phone']
        if 'address' in data:
            customer.address = data['address']
        if 'membership_id' in data:
            customer.membership_id = data['membership_id']
        
        return jsonify(customer.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a customer"""
    customer = find_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    customers.remove(customer)
    return jsonify({'message': 'Customer deleted successfully'}), 200

# Create a route to search customers by name or email
@customer_bp.route('/search', methods=['GET'])
def search_customers():
    """Search customers by name or email"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400
    
    matched_customers = [
        customer.to_dict() for customer in customers
        if query in customer.first_name.lower() or
           query in customer.last_name.lower() or
           query in customer.email.lower()
    ]
    
    return jsonify(matched_customers)