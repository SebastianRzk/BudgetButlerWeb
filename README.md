# BudgetButlerWeb

[![Build Status](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb.svg?branch=master)](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb) [![codecov](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb/branch/master/graph/badge.svg)](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb)

## Documentation

[Link to the project page on github](https://RosesTheN00b.github.io/BudgetButlerWeb/)

## local app
### Requirements

* Python 3.6
* Pip
* Modern Webbrowser (e.G. Firefox or Chromium)
* (git)

### Install and run 
Clone the repository:

	git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

Change into project directory

	cd BudgetButlerWeb

Install the requirements

	pip install -r requirements.txt

Run offline applicaton server:

	sh start_butler_offline.sh

Open your webbrowser and visit:

	http://127.0.0.1:5000/


## online app

### Requirements

* Database
* PHP-server

### Installation

* Clone the repository

	git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

* Change into project directory

	cd BudgetButlerWeb/butler_online

* Install the requirements

	composer install

* Create the database on your server

* Change into online installation directory and run

    cd ../online_install
    pip install -r requirements.txt

* Execute the database install script:

    python install_database.py

* Change the host in `butler_online/db.ini` if necessary

* Load the contents of the `butler_online` folder onto the server

* Check permissions. Make sure that the file `db.ini` can not be accessed.

* Login on `/login.php`. Initial credentials are:
    * User: admin@admin.de 
    * Password: admin`

## Screenshots
[Link to screenshots page](docs/screenshots.md)

## TODO
[Link to todo page](docs/todo.md)


