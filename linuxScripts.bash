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
    newPhrase="baseUrl:'192.168.1.72:8000',"
    sed -i 's/baseUrl:.*/'"$newPhrase"'/g' frontend/pages/index.tsx
    pip install -r requirements.txt
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py test
    if [ $? = 0 ]; then
        screen -S DjangoAPI -d -m python3 manage.py runserver 192.168.1.72:8000
        screen -S Next -d -m bash -c "npm run build --prefix frontend; npm run start --prefix frontend"
        screen -S cWorker -d -m celery -A daytrader worker -l info
        screen -S cBeat -d -m celery -A daytrader beat
        screen -ls
    else
        echo "Tests failed, fix errors and restart server"
    fi

elif [[ $1 == "help" ]]
then
    showHelp
else
    echo "Please select a command to run"
fi