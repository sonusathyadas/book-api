import pytest
import json
from app import app
from models.customer import Customer
import customer_routes


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Reset the customers list to initial state for each test
            customer_routes.customers.clear()
            customer_routes.customers.extend([
                Customer(1, "John", "Doe", "john.doe@email.com", "555-0101", "123 Main St, Anytown, USA"),
                Customer(2, "Jane", "Smith", "jane.smith@email.com", "555-0102", "456 Oak Ave, Somewhere, USA"),
                Customer(3, "Bob", "Johnson", "bob.johnson@email.com", "555-0103", "789 Pine Rd, Anywhere, USA"),
                Customer(4, "Alice", "Williams", "alice.williams@email.com", "555-0104", "321 Elm St, Nowhere, USA"),
                Customer(5, "Charlie", "Brown", "charlie.brown@email.com", "555-0105", "654 Maple Dr, Everywhere, USA")
            ])
            yield client


class TestGetAllCustomers:
    """Test cases for GET /api/customers endpoint."""
    
    def test_get_all_customers_success(self, client):
        """Test successful retrieval of all customers."""
        response = client.get('/api/customers/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 5
        assert data[0]['first_name'] == "John"
        assert data[0]['last_name'] == "Doe"
        assert data[0]['email'] == "john.doe@email.com"
        
    def test_get_all_customers_returns_json(self, client):
        """Test that the response is valid JSON."""
        response = client.get('/api/customers/')
        assert response.content_type == 'application/json'
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        for customer in data:
            assert 'id' in customer
            assert 'first_name' in customer
            assert 'last_name' in customer
            assert 'email' in customer
            assert 'phone' in customer
            assert 'address' in customer


class TestGetCustomerById:
    """Test cases for GET /api/customers/<id> endpoint."""
    
    def test_get_customer_by_id_success(self, client):
        """Test successful retrieval of a customer by ID."""
        response = client.get('/api/customers/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['first_name'] == "John"
        assert data['last_name'] == "Doe"
        assert data['email'] == "john.doe@email.com"
        
    def test_get_customer_by_id_not_found(self, client):
        """Test retrieval of non-existent customer."""
        response = client.get('/api/customers/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Customer not found'
        
    def test_get_customer_by_id_edge_cases(self, client):
        """Test edge cases for customer retrieval."""
        # Test with zero ID
        response = client.get('/api/customers/0')
        assert response.status_code == 404
        
        # Test with negative ID
        response = client.get('/api/customers/-1')
        assert response.status_code == 404


class TestCreateCustomer:
    """Test cases for POST /api/customers endpoint."""
    
    def test_add_customer_success(self, client):
        """Test successful creation of a new customer."""
        new_customer_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@email.com',
            'phone': '555-1234',
            'address': '123 Test St, Test City, USA'
        }
        
        response = client.post('/api/customers/',
                              data=json.dumps(new_customer_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['first_name'] == 'Test'
        assert data['last_name'] == 'User'
        assert data['email'] == 'test.user@email.com'
        assert data['phone'] == '555-1234'
        assert data['address'] == '123 Test St, Test City, USA'
        assert 'id' in data
        assert data['id'] == 6  # Should be next ID after 5
        
    def test_add_customer_missing_required_fields(self, client):
        """Test creation with missing required fields."""
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        
        for field in required_fields:
            incomplete_data = {
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@email.com',
                'phone': '555-1234',
                'address': '123 Test St'
            }
            del incomplete_data[field]
            
            response = client.post('/api/customers/',
                                  data=json.dumps(incomplete_data),
                                  content_type='application/json')
            assert response.status_code == 400
            
            data = json.loads(response.data)
            assert f'Missing required field: {field}' in data['error']
            
    def test_add_customer_no_json_data(self, client):
        """Test creation without JSON data."""
        response = client.post('/api/customers/')
        assert response.status_code == 400


class TestUpdateCustomer:
    """Test cases for PUT /api/customers/<id> endpoint."""
    
    def test_update_customer_success(self, client):
        """Test successful update of a customer."""
        update_data = {'first_name': 'Updated'}
        
        response = client.put('/api/customers/1',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['first_name'] == 'Updated'
        assert data['last_name'] == 'Doe'  # Should remain unchanged
        assert data['id'] == 1
        
    def test_update_customer_all_fields(self, client):
        """Test update of all customer fields."""
        update_data = {
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'email': 'updated@email.com',
            'phone': '555-9999',
            'address': 'Updated Address'
        }
        
        response = client.put('/api/customers/1',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['first_name'] == 'UpdatedFirst'
        assert data['last_name'] == 'UpdatedLast'
        assert data['email'] == 'updated@email.com'
        assert data['phone'] == '555-9999'
        assert data['address'] == 'Updated Address'
        
    def test_update_customer_not_found(self, client):
        """Test update of non-existent customer."""
        update_data = {'first_name': 'Updated'}
        
        response = client.put('/api/customers/999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['error'] == 'Customer not found'
        
    def test_update_customer_empty_data(self, client):
        """Test update with empty data."""
        response = client.put('/api/customers/1',
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 200
        
        # Customer should remain unchanged
        data = json.loads(response.data)
        assert data['first_name'] == 'John'
        assert data['last_name'] == 'Doe'


class TestDeleteCustomer:
    """Test cases for DELETE /api/customers/<id> endpoint."""
    
    def test_delete_customer_success(self, client):
        """Test successful deletion of a customer."""
        response = client.delete('/api/customers/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['message'] == 'Customer deleted successfully'
        
        # Verify customer is actually deleted
        response = client.get('/api/customers/1')
        assert response.status_code == 404
        
    def test_delete_customer_not_found(self, client):
        """Test deletion of non-existent customer."""
        response = client.delete('/api/customers/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['error'] == 'Customer not found'
        
    def test_delete_customer_multiple_deletions(self, client):
        """Test that multiple customers can be deleted."""
        # Delete customer 1
        response = client.delete('/api/customers/1')
        assert response.status_code == 200
        
        # Delete customer 2
        response = client.delete('/api/customers/2')
        assert response.status_code == 200
        
        # Verify both are deleted
        response = client.get('/api/customers/')
        data = json.loads(response.data)
        assert len(data) == 3  # Should have 3 remaining customers


class TestHelperFunctions:
    """Test cases for helper functions."""
    
    def test_find_customer_by_id(self, client):
        """Test the find_customer_by_id helper function."""
        customer = customer_routes.find_customer_by_id(1)
        assert customer is not None
        assert customer.first_name == "John"
        assert customer.last_name == "Doe"
        
        customer = customer_routes.find_customer_by_id(999)
        assert customer is None
        
    def test_get_next_customer_id(self, client):
        """Test the get_next_customer_id helper function."""
        next_id = customer_routes.get_next_customer_id()
        assert next_id == 6  # Should be max(5) + 1
        
        # Add a customer and test again
        new_customer = Customer(10, "Test", "User", "test@email.com", "555-0000", "Test Address")
        customer_routes.customers.append(new_customer)
        
        next_id = customer_routes.get_next_customer_id()
        assert next_id == 11  # Should be max(10) + 1


class TestIntegrationScenarios:
    """Integration test scenarios combining multiple operations."""
    
    def test_create_update_delete_flow(self, client):
        """Test complete CRUD flow for a customer."""
        # Create a new customer
        new_customer_data = {
            'first_name': 'Integration',
            'last_name': 'Test',
            'email': 'integration@test.com',
            'phone': '555-9999',
            'address': 'Integration Test Address'
        }
        
        response = client.post('/api/customers/',
                              data=json.dumps(new_customer_data),
                              content_type='application/json')
        assert response.status_code == 201
        
        created_customer = json.loads(response.data)
        customer_id = created_customer['id']
        
        # Update the customer
        update_data = {'first_name': 'Updated Integration'}
        response = client.put(f'/api/customers/{customer_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        updated_customer = json.loads(response.data)
        assert updated_customer['first_name'] == 'Updated Integration'
        
        # Delete the customer
        response = client.delete(f'/api/customers/{customer_id}')
        assert response.status_code == 200
        
        # Verify deletion
        response = client.get(f'/api/customers/{customer_id}')
        assert response.status_code == 404