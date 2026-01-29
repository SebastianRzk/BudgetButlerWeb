#!/bin/bash
set -ue

APPDIR="AppDir"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/budgetbutlerweb/static"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$APPDIR/usr/share/licenses/budgetbutlerweb"
mkdir -p "$APPDIR/usr/share/metainfo"

cp target/budgetbutlerweb "$APPDIR/usr/bin/budgetbutlerweb-backend"
cp application-wrapper/BudgetButlerWeb-AppRun "$APPDIR/AppRun"

if [ -f "$APPDIR/AppRun" ]; then
  chmod +x "$APPDIR/AppRun"
fi

cp -r target/static/* "$APPDIR/usr/share/budgetbutlerweb/static/"

cp -r target/application-wrapper/* "$APPDIR/usr/share/budgetbutlerweb/"

cp de.sebastianruziczka.budgetbutlerweb.metainfo.xml "$APPDIR/usr/share/metainfo/de.sebastianruziczka.budgetbutlerweb.appdata.xml"

cp icon/BudgetButlerWeb_256.png "$APPDIR/usr/share/icons/hicolor/256x256/apps/de.sebastianruziczka.budgetbutlerweb.png"

cp application-wrapper/BudgetButlerWeb.desktop "$APPDIR/de.sebastianruziczka.budgetbutlerweb.desktop"

cp LICENSE "$APPDIR/usr/share/licenses/budgetbutlerweb/LICENSE"

if [ ! -f linuxdeploy ]; then
  wget -O linuxdeploy https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
  chmod +x linuxdeploy
fi

./linuxdeploy --appdir "$APPDIR" -d "$APPDIR/de.sebastianruziczka.budgetbutlerweb.desktop" -i "$APPDIR/usr/share/icons/hicolor/256x256/apps/de.sebastianruziczka.budgetbutlerweb.png" --output appimage

echo "AppImage gebaut: $(ls *.AppImage)"
