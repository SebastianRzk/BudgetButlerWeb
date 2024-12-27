#! /bin/sh


echo "creating [Desktop Entry]"

echo "[Desktop Entry]
Type=Application
Name=BudgetButlerWeb
GenericName=Simple and fast money manager
Icon=$HOME/.local/share/icons/budgetbutlerweb-logo.png
Path=$PWD/target/
Terminal=false
Exec=bash -c 'cd \"$PWD/target/\" && $PWD/target/application-wrapper/budgetbutlerweb'" >   ~/.local/share/applications/BudgetButlerWeb.desktop

cp ./application-wrapper/BudgetButlerWeb/src/BBFav.png ~/.local/share/icons/budgetbutlerweb-logo.png

echo "Done";
