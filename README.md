# Birdvision Submission

## Features

- User authentication with JWT tokens
- Product management (CRUD operations)
- Pagination support for product listing
- SQLite database integration
- Automated tests with Pytest

## Installation

To get started with the Birdvision Submission project, follow these steps:

### Prerequisites

- Python 3.8 or higher
- pip and virtualenv

### Setting Up a Virtual Environment

- To create a virtual environment, navigate to the project's root directory and run:
`python -m venv venv`
- Activate the virtual environment:
- On Windows: `.\venv\Scripts\activate`
- On macOS and Linux: `source venv/bin/activate`

### Installing Dependencies

`pip install -r requirements.txt`

## Running the Application

`uvicorn main:app --reload`

## Accessing the Application

- Application: `http://localhost:8000`
- API Documentation (Swagger UI): `http://localhost:8000/docs`

### Important

- When signing up, email should be according to email standard
- Password should be minimum 8 characters long, with combination of numbers, alphabets (upper and lowercase) and special characters, according to python's inbuilt password check

## Running Tests

`pytest .\tests\test.py`

## Environment Variables

Create a `.env` file in the project's root directory with the following variables:
```
DATABASE_URL=sqlite:///./products.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Project Structure

Describe your project structure here.

```
.
├── main.py                # FastAPI application entry point
├── models                 # Database models and Pydantic schemas
│   ├── db.py              # Database setup and session management
│   └── models.py          # Pydantic schemas for request and response models
├── resource               # Authentication helpers and business logic
│   └── auth_helper.py     # Helper functions for authentication
├── routes                 # Application routes
│   ├── auth.py            # Authentication endpoints
│   └── product.py         # Product management endpoints
├── tests                  # Automated tests
│   └── test.py            # Test suite for the application
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation (this file)
```
