# FastAPI Users and Orders API

A RESTful API built with FastAPI for managing users and their orders. This API provides CRUD (Create, Read, Update, Delete) operations for both users and orders with proper error handling and data validation.

## Features

- CRUD operations for Users and Orders
- Data validation using Pydantic models
- SQLAlchemy ORM for database operations
- Comprehensive error handling
- Automated tests using pytest
- SQLite database (configurable to use PostgreSQL)
- API documentation with Swagger UI

## Prerequisites

- Python 3.7+
- virtualenv (recommended)

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI application and routes
│   ├── models.py       # SQLAlchemy models
│   ├── schemas.py      # Pydantic models
│   └── database.py     # Database configuration
├── tests/
│   ├── __init__.py
│   └── test_main.py    # Test cases
└── README.md
```

## Installation

1. Clone the repository:

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi[all] sqlalchemy pydantic[email] pytest httpx
```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Orders
- `POST /orders/` - Create a new order
- `GET /orders/{id}` - Get order by ID
- `PUT /orders/{id}` - Update order
- `DELETE /orders/{id}` - Delete order

## Running Tests

```bash
python -m pytest -v
```

## Database Configuration

The application uses SQLite by default. To switch to PostgreSQL:

1. Update the database URL in `app/database.py`:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

2. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

## Error Handling

The API includes handling for:
- Invalid input data
- Resource not found
- Duplicate email addresses
- Database constraints
- Invalid quantities for orders

## Development Notes

- The application uses Pydantic for data validation
- SQLAlchemy is used as the ORM
- Tests use an in-memory SQLite database
- API responses are properly typed using Pydantic models

