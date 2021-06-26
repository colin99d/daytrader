# daytrader
1. Required installs postgres, redis, celery
    1. For Mac:
        1. brew install postgresql
        1. brew install redis
        1. brew install celery

1. Create a database:
    1. createdb daytrader
    1. psql
    1. CREATE ROLE myusername WITH LOGIN PASSWORD 'mypassword';
    1. GRANT ALL PRIVILEGES ON DATABASE daytrader TO myusername;
    1. ALTER USER myusername CREATEDB;

1. Start Celery
    1. celery -A daytrader worker -l info
    1. celery -A daytrader beat

1. Run coverage report
    1. coverage run --source='.' manage.py test
    1. coverage html
    1. The main report is in htmlcov/index.html