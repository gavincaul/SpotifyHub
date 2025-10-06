#!/bin/sh 
if lsof -i :4000 >/dev/null; then 
    echo "Port 4000 in use. Killing existing process..." 
    kill -9 $(lsof -t -i :4000) 
fi 
export FLASK_APP=./src/backend/app.py 
export FLASK_ENV=development 
flask run --port=4000 --host=localhost &

