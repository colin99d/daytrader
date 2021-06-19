#brew services start postgresql
#brew services start mailhog
#brew services start redis

workon daytrader && celery -A daytrader  worker -l info
workon daytrader && celery -A daytrader beat