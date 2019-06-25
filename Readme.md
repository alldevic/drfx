# DRFx

A framework for launching new Django Rest Framework projects quickly. Comes with login/logout/signup, jwt support and more

## Features

- Django 2.2 and Python 3.6
- Custom user model
- Token-based auth
- Signup/login/logout
- [djangorestframework-jsonapi](https://github.com/django-json-api/django-rest-framework-json-api) for JSON API support
- [django-filters](https://github.com/carltongibson/django-filter) for Django ORM-style JSON:API filter
- [drf-yasg](https://github.com/axnsan12/drf-yasg) for automated generation of real Swagger/OpenAPI 2.0 schemas from Django REST Framework code.
- [djoser](https://github.com/sunscrapers/djoser) for authentication support
- [django-rest-framework-simplejwt](https://github.com/davesque/django-rest-framework-simplejwt) for JWT support
- [Pipenv](https://github.com/pypa/pipenv) for virtualenvs

## First-time setup

1.  Make sure Python 3.6x and Pipenv are already installed. [See here for help](https://djangoforbeginners.com/initial-setup/).
2.  Clone the repo and configure the virtual environment:

```
$ git clone https://github.com/alldevic/drfx.git
$ cd drfx
$ pipenv install
$ pipenv shell
```

3.  Set up the initial migration for our custom user models in users and build the database.

```
(drfx) $ python manage.py makemigrations users
(drfx) $ python manage.py migrate
(drfx) $ python manage.py createsuperuser
(drfx) $ python manage.py runserver
```

4.  Endpoints

Login with your superuser account. Then navigate to all users. Logout. Sign up for a new account and repeat the login, users, logout flow.

- base and token djoser urls
- swagger UI - http://127.0.0.1:8000/swagger/
- swagger.yaml file - http://127.0.0.1:8000/swagger.yaml
- swagger.json file - http://127.0.0.1:8000/swagger.json
- redoc UI - http://localhost:8000/redoc/
