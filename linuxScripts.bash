showHelp() {
cat << EOF

[command]

runserver       Starts Django API, Next.js App, and Celery worker/beat

[arguments]
EOF
}

if [[ $1 == "runserver" ]]
then
    screen -S DjangoAPI -d -m python3 manage.py runserver 192.168.1.72:8000
    screen -S Next -d -m npm run dev --prefix frontend
    screen -S cWorker -d -m celery -A daytrader worker -l info
    screen -S cBeat -d -m celery -A daytrader beat

elif [[ $1 == "collectstatic" ]]
then
    echo "Feature not implemented"
else
    echo "Please select a command to run"
fi