#!/bin/sh
echo "Starting BudgetButlerWeb local server"
cd butler_offline
export FLASK_APP=start_as_flask.py 
flask run
