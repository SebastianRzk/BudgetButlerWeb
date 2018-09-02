#!/bin/sh
echo "Starting BudgetButlerWeb local server"
export FLASK_APP=start_as_flask.py 
flask run
