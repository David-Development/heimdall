#! /bin/sh

if [ `whoami` != root ]; then
    echo Please run this script as root or using sudo
    exit
fi

docker-compose stop

docker pull luhmer/opencv-python3
docker pull luhmer/heimdall-backend
docker pull luhmer/heimdall-frontend

git pull
git submodule init
git submodule update --recursive --remote

# reboot
