# daytrader

Daytrader is an intermediate Django project meant to showcase various intermediate level skills in Django. This project is run in Docker and is setup to use NGINX and Uvicorn in production. To handle taks querying Daytrader uses Celery and Redis. Daytrader also uses Channels to handle websocket connections. The frontend is a Next.js React app written in TypeScipt and uses the Tailwind CSS framework. Please see the notes below to run the application.

1. Run coverage report
    1. coverage run --source='.' manage.py test
    1. coverage html
    1. The main report is in htmlcov/index.html

1. Docker:
    1. Local:
        1. docker-compose up -d --build
    1. Production:
        1. Build/up: docker-compose -f docker-compose.prod.yml up -d --build
        1. Migrate: docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
        1. Kill: docker-compose -f docker-compose.prod.yml down -v
    1. See logs:
        1. Use 'docker ps' to see al container names
        1. Use 'docker logs -f [name or id of container]' to see logs from server
    1. Fix Database error (column does not exist)
        1. docker-compose -f "compose file" run --rm django python manage.py migrate tables zero
        1. docker-compose -f "compose file" --rm django python manage.py migrate


