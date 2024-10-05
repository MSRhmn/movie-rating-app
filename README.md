# Movie Rating App

## Overview
This application is a RESTful API built with `Django REST Framework` that allows users to:
- User registration and authentication
- CRUD operations for movies
- Rating system for movies
- Permissions to ensure only authenticated users can rate movies
- Browsable API for easy testing and interaction

## Features
- User authentication and authorization
- Error handling with appropriate HTTP status codes
- Data validation for user input

## Technology Stack
- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+

## Installation and Usage
1. Clone this repository:
`git clone https://github.com/MSRhmn/movie-rating-app.git`
`cd movie-rating-app`
2. Create and activate a virtual environment:
`python/python3/py -m venv venv`
`source venv/bin/activate`  # On Windows use `venv\Scripts\activate`
3. Install required dependencies:
`pip install -r requirements.txt`
4. Run migrations:
`python manage.py migrate`
6. Start the development server:
`python manage.py runserver`

## Interact with the API using the tool `curl`:

### Register a new user
`curl -X POST http://localhost:8000/api/v1/register/ -H "Content-Type: application/json" -d '{"username": "newuser", "password": "newpassword", "email": "newuser@example.com"}'`

### Login Endpoint
`curl -X POST http://localhost:8000/api/v1/login/ -H "Content-Type: application/json" -d '{"username": "newuser", "password": "newpassword"}'`

### Get Movies Endpoint
`curl -X GET http://localhost:8000/api/v1/movies/`

### Get Movie Endpoint by ID 
`curl -X GET http://localhost:8000/api/v1/movies/1/`

### Add Movie Endpoint
`curl -X POST http://localhost:8000/api/v1/movies/ -H "Content-Type: application/json" -H "Authorization: Token 743c92c2b90be460fe7ae522a18d9cb4373884d1" -d '{"title": "The Croods", "genre": "Animation", "rating": 0, "release_date": "2013-03-22"}'`

### Rate Movie Endpoint
`curl -X POST http://localhost:8000/api/v1/movies/4/rate/ -H "Content-Type: application/json" -H "Authorization: Token 743c92c2b90be460fe7ae522a18d9cb4373884d1" -d '{"rating": 8}'`
