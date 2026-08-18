# Rides API

A RESTful API for managing users, rides, and ride events. Created using Django REST Framework

## Tech Stack

- Python 3.13
- Django 6.1
- Django REST Framework
- drf-spectacular
- django-filter

# Initial Setup

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## API docs
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

