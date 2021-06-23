showHelp() {
cat << EOF

[command]

runserver       Starts Django API, Next.js App, and Celery worker/beat

[arguments]
EOF
}

if [[ $1 == "runserver" ]]
then
    screen python3 manage.py runserver 192.168.1.72:8000
    cd frontend && screen npm run dev -H 192.168.1.72
    gnome-terminal -x bash -c "cd frontend && npm run dev -H 192.168.1.72; exec bash"
    gnome-terminal -x bash -c "celery -A daytrader worker -l info"
    gnome-terminal -x bash -c "celery -A daytrader beat"

elif [[ $1 == "collectstatic" ]]
then
    echo "Feature not implemented"
else
    echo "Please select a command to run"
fi