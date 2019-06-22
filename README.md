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

#### Server requirements

* Database
* PHP-server

#### Building requirements

* npm
* composer

### Installation

* Clone the repository

	git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

* Change into project directory

	cd BudgetButlerWeb

* Trigger the install into `butler_all_online_distribution`

	sh butler_all_online_install/compose.sh

* Change the database credentials in `butler_all_online_distribution/api/db.ini` if necessary

* Load the content of the `butler_all_online_distribution` folder onto the server

* install the sql from `butler_all_online_install/`

* Check permissions. Make sure that the file `db.ini` can not be accessed.

* Login on `/login.php`. Initial credentials are:
    * User: admin@admin.de 
    * Password: adminadminadmin

## Screenshots
[Link to screenshots page](docs/screenshots.md)

## TODO
[Link to todo page](docs/todo.md)


