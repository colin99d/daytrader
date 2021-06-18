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