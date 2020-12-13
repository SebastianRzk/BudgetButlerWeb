# BudgetButlerWeb

[![Build Status](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb.svg?branch=master)](https://travis-ci.org/RosesTheN00b/BudgetButlerWeb) [![codecov](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb/branch/master/graph/badge.svg)](https://codecov.io/gh/RosesTheN00b/BudgetButlerWeb)

## Documentation

[Link to the project page on github](https://RosesTheN00b.github.io/BudgetButlerWeb/)

## Local app
### Requirements

* Python 3.6
* Pip
* Chromium (if you don't want to use the .desktop shortcut, you can use any modern browser)
* Startup script: shell, curl, Chromium
* Versioning: git

### Install and run 
Clone the repository:

	git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

Change into project directory

	cd BudgetButlerWeb

(Optional) Create a application shortcut with

	sh ./create_shortcut.sh

Or start the application with:

	sh start_butler_offline.sh

And open your webbrowser and visit:

	http://127.0.0.1:5000/


## Companion web app

### Requirements

#### Server requirements

* Database
* PHP-server (7.3+)

or

* docker and docker-compose

#### Building requirements

* npm
* composer

### Installation

* Clone the repository

	git clone https://github.com/RosesTheN00b/BudgetButlerWeb.git

* Change into project directory

	cd BudgetButlerWeb

* Trigger the install into `butler_online_distribution`

	sh butler_online_install/compose.sh

* Change the database credentials in `butler_online_distribution/api/db.ini` if necessary

* For webspace edition:

    * Load the content of the `butler_online_distribution/webspace_edition` folder onto the server

    * install the sql from `butler_online_install/`

    * Check permissions. Make sure that the file `db.ini` can not be accessed.

* For docker-compose:

    * call `docker-compose up` in `butler_online_distribution/docker-edition/budget_butler`

* Login on `/`. Initial credentials are:
    * User: admin@admin.de 
    * Password: adminadminadmin

### Update

* To update the docker server, run `butler_online_install/compose_incremental.sh` and in the docker-compose directory `docker-compose up -d --force-recreate --build`

## Screenshots
[Link to screenshots page](docs/screenshots.md)


