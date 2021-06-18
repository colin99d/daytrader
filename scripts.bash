workon daytrader
brew services start postgresql
brew services start redis
celery -A daytrader  worker -l info
celery -A daytrader beat
brew services start mailhog