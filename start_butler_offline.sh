#!/bin/sh

set -e

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
VENV_DIR=$parent_path/.venv
HOST=http://localhost:5000

export FLASK_APP=start_as_flask.py


if [[ ! -d $VENV_DIR ]]; then
    echo ""
    echo "#################################"
    echo "#### BudgetButlerWeb offline ####"
    echo "######### Installation ##########"
    echo "#################################"
    echo "#################################"
    echo ""

    python -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    pip install -r $parent_path/butler_offline/requirements.txt

    echo ""
    echo "#################################"
    echo "#### BudgetButlerWeb offline ####"
    echo "############ Ready  #############"
    echo "#################################"
    echo "#################################"
    echo ""
fi

source $VENV_DIR/bin/activate

echo ""
echo "#################################"
echo "#### BudgetButlerWeb offline ####"
echo "######### Starting ...  #########"
echo "#################################"
echo "#################################"
echo ""

echo "Starting BudgetButlerWeb local server"
cd "$parent_path/butler_offline"

flask run &

tries=0
until $(curl --output /dev/null --silent --head --fail $HOST); do
    echo "Waiting for server to be up..."

    tries=$tries+1
    if [[ tries -gt 20 ]]; then
        echo "Server is not coming up. Exiting..."
        exit 1
    fi

    sleep 1
done

chromium --app=$HOST

pkill -P $$
