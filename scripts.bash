#brew services start postgresql
#brew services start mailhog
#brew services start redis

text=$(env | grep PYENV_VIRTUAL_ENV)
echo $text
IFS='/' 
read -ra arr <<< $text

daytrader
celery -A daytrader  worker -l info

osascript -e "
    tell application \"Terminal\"
    set currentTab to do script \"cd $(pwd)\"
    do script \"pyenv start daytrader\" in currentTab
    do script \"celery -A daytrader beat\" in currentTab
    end tell"
