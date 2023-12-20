  #!/bin/sh

set -e

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
VENV_DIR=$parent_path/venv
NODE_DIR=$parent_path/butler_offline_client/node_modules
HOST=http://localhost:5000

echo ""
echo "#################################"
echo "#### BudgetButlerWeb offline ####"
echo "###### Check dependencies #######"
echo "#################################"
echo "#################################"
echo ""


if [[ ! -d $VENV_DIR ]]; then
    python -m venv $VENV_DIR
fi


source $VENV_DIR/bin/activate
pip install -r $parent_path/butler_offline/requirements.txt

cd $parent_path
flask --app butler_offline run &
deactivate

cd $parent_path/butler_offline_client

if [[ ! -d $NODE_DIR ]]; then
    npm install
fi

npm run start

pkill -P $$
