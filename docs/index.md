# BudgetButlerWeb
[![Build Status](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb.svg?branch=master)](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb) [![codecov](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb/branch/master/graph/badge.svg)](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb)

## Requirements

* Python 3.6
* Pip
* Modern Webbrowser (e.G. Firefox or Chromium)
* (git)

## Install and run
Clone the repository:

	git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

Change into project directory

	cd BudgetButlerWeb

Install the requiurements

	pip install -r requirements.txt

Change into django module and run server:

	cd mysite
	python manage.py runserver

Open your webbrowser and visit:

	http://127.0.0.1:8000/
	
## Run tests

Run all softwaretests with pytest:

	pytest

Run tests with coverage analysis:

	py.test --cov=mysite

## Known problems

* Google Chrome: Wrong vertical sizing of charts

## TODO
[Link to todo page](todo.md)


