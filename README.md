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
python manage.py test
python manage.py runserver 0.0.0.0:8000
```

## API docs
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Authentication

All of the API endpoint requires an authenticated user with a role `admin`.

```cmd
python manage.py createsuperuser
```

## User API

```text
GET /api/users/
```

## Ride Event API

```text
GET /api/rides/events/
```

## Ride API

```text
GET /api/rides/
```

The ride list supports filtering, sorting, and pagination.

Each ride response includes rider, driver, and recent ride events

- `rider` - Full details about id_rider from `id_rider` 
- `driver` - Full details about id_driver from `id_driver`
- `todays_ride_events` - RideEvents created within the past 24 hours

### Filtering

Filter by status:

```text
GET /api/rides/?status=pickup
```

Filter by rider email:

```text
GET /api/rides/?rider_email=rider@example.com
```

Both filters can also be used together:

```text
GET /api/rides/?status=pickup&rider_email=rider@example.com
```

### Sorting

Sort by pickup time:

```text
GET /api/rides/?ordering=pickup_time
GET /api/rides/?ordering=-pickup_time
```

Sort by distance from given pickup location:

```text
GET /api/rides/?ordering=distance&pickup_lat=14.5995&pickup_lng=120.9842
GET /api/rides/?ordering=-distance&pickup_lat=14.5995&pickup_lng=120.9842
```

Distance will be calculated using Django `ExpressionWrapper` and spherical law of cosines formula

### Pagination

API use limit-offset pagination:

```text
GET /api/rides/?limit=25&offset=0
GET /api/rides/?limit=25&offset=25
```

Filtering, sorting, and pagination can be used together:

```text
GET /api/rides/?status=pickup&ordering=pickup_time&limit=25&offset=0
GET /api/rides/?ordering=distance&pickup_lat=14.5995&pickup_lng=120.9842&limit=25&offset=0
```
