showHelp() {
cat << EOF

[command]

runserver       Starts Django API, Next.js App, and Celery worker/beat

[arguments]
EOF
}

if [[ $1 == "runserver" ]]
then
    pkill screen
    pip install -r requirements.txt
    python3 manage.py makemigrations
    python3 manage.py migrate
    screen -S DjangoAPI -d -m python3 manage.py runserver 192.168.1.72:8000
    screen -S Next -dm -c 'npm run build; npm run start --prefix frontend;'
    screen -S cWorker -d -m celery -A daytrader worker -l info
    screen -S cBeat -d -m celery -A daytrader beat
    screen -ls

elif [[ $1 == "collectstatic" ]]
then
    echo "Feature not implemented"
else
    echo "Please select a command to run"
fi