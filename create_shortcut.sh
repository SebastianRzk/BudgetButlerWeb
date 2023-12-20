#!/bin/bash

rm -f budgetbutler.desktop

echo "[Desktop Entry]" >> budgetbutler.desktop
echo "Encoding=UTF-8" >> budgetbutler.desktop
echo "Version=1.0" >> budgetbutler.desktop
echo "Type=Application" >> budgetbutler.desktop
echo "Terminal=false" >> budgetbutler.desktop
echo "Exec=$(pwd)/start_butler_offline.sh" >> budgetbutler.desktop
echo "Name=BudgetButler" >> budgetbutler.desktop
echo "Comment=Simple money manager" >> budgetbutler.desktop
echo "Icon=$(pwd)/butler_offline/static/BBFav.png" >> budgetbutler.desktop

mv budgetbutler.desktop ~/.local/share/applications
