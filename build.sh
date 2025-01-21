#!/bin/bash
set -ue

pushd butler_offline
cargo build --release
popd

pushd application-wrapper/BudgetButlerWeb/
npm install
npm run package
popd

echo "delete old target"
rm -rf target
echo "old target deleted"

echo "creating new target"
mkdir -p target
cp butler_offline/target/release/budgetbutlerweboffline target/budgetbutlerweb
mkdir -p target/static
cp -rf butler_offline/static/* target/static
mkdir -p target/application-wrapper
cp -r application-wrapper/BudgetButlerWeb/out/budgetbutlerweb-linux-x64/* target/application-wrapper

echo "done";
