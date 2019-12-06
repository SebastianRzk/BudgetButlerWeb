#!/bin/sh

echo "Starting BudgetButlerWeb local server"
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path/butler_offline"
export FLASK_APP=start_as_flask.py 

eval  "sleep 4s && chromium --app=http://localhost:5000" &
flask run

