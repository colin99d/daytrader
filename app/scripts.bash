#brew services start postgresql
#brew services start mailhog
#brew services start redis

showHelp() {
cat << EOF

[command]

runserver       Starts Django API, Next.js App, and Celery worker/beat

[arguments]
EOF
}

if [[ $1 == "runserver" ]]
then
    pyenv shell daytrader
    python3 manage.py runserver
    osascript -e "
        tell application \"Terminal\"
        set currentTab to do script \"cd $(pwd)\"
        do script \"cd frontend\" in currentTab
        do script \"npm run dev\" in currentTab"
    osascript -e "
        tell application \"Terminal\"
        set currentTab to do script \"cd $(pwd)\"
        do script \"pyenv activate daytrader\" in currentTab
        do script \"celery -A daytrader worker -l info\" in currentTab
        end tell"
    osascript -e "
        tell application \"Terminal\"
        set currentTab to do script \"cd $(pwd)\"
        do script \"pyenv activate daytrader\" in currentTab
        do script \"celery -A daytrader beat\" in currentTab
        end tell"
elif [[ $1 == "collectstatic" ]]
then
    echo "Feature not implemented"
else
    echo "Please select a command to run"
fi


