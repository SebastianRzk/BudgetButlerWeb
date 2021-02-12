#!/bin/bash
set -e

echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~Start  Building~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~BudgetButlerWeb~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"

rm -rfv ./butler_online_distribution

sh ./butler_online_install/build_assets.sh
sh ./butler_online_install/create_docker_bind_distribution.sh
sh ./butler_online_install/create_docker_images_distribution.sh
sh ./butler_online_install/create_docker_webspace_distribution.sh

echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~~Done Building~~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~BudgetButlerWeb~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"

