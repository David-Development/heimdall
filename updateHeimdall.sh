#! /bin/sh

if [ `whoami` == root ]; then
    echo "Please do not run this script as root or using sudo"
    exit
fi

docker-compose stop

git pull
git submodule init
git submodule update --recursive --remote

#docker pull luhmer/opencv-python3
#docker pull luhmer/heimdall-backend
#docker pull luhmer/heimdall-frontend
#docker pull luhmer/emqtt
docker-compose pull

# reboot
