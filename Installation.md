# Table of Content

- Setup
  - docker/docker-compose installation instructions
  - Clone repo / Pull docker images
  - Start heimdall using RTSP / MQTT / TCP-Socket Camera
    - RTSP cameras
    - TCP cameras
    - MQTT cameras
  - (Optional) Installation instructions for Low-Energy Camera developed at the Bonn-Rhein-Sieg University)
    - Start heimdall using the low-energy camera
- Useful Commands for debugging/testing/development




# Setup

- System was tested on XUbuntu 16.04.3 - It took me around 30 minutes to install XUbuntu as well as heimdall on an Intel NUC Computer. Installing and setting up the camera may take some more time.


## Install Docker & Docker Compose

- Run `installDocker.sh` file from the root of the heimdall project or follow the installation instructions on [docs.docker.com](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository)

## Give non-root user permission to execute docker

```
sudo groupadd docker
sudo usermod -aG docker $USER # Add sudo to group docker
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "/home/$USER/.docker" -R
reboot
```

## Clone this repo

```sh
cd /home/heimdall/Desktop
git clone --recursive https://github.com/David-Development/heimdall.git
```

## Pull Heimdall Docker Images

```sh
docker pull luhmer/opencv-python3
docker pull luhmer/heimdall-backend
docker pull luhmer/heimdall-frontend
docker pull luhmer/emqtt
```


### Setup Heimdall to start while booting

- `sudo nano /etc/rc.local`
- Append the following code snippet (before the `exit 0` line)

```sh
sh /home/heimdall/Desktop/heimdall/startHeimdall.sh > /home/heimdall/Desktop/heimdall-log.txt 2>&1 &
exit 0
```

#### Access log file

After starting the docker-containers (as shown below) you can view the log files by opening the `heimdall-log.txt`

`tail -f -n 100 heimdall-log.txt`




## Start Heimdall (using RTSP / MQTT / TCP-Socket Camera)

Beside the low-enery camera developed at the Bonn-Rhein-Sieg University, Heimdall also supports RTSP, MQTT as well as TCP-Socket cameras. 

### RTSP Cameras

Edit the `docker-compose.yaml` file. Adjust the `RTSP_HOST` variable according to your environment in the `heimdall-camera-rtsp` service definition.

```bash
# Change into the directory where you downloaded heimdall to
cd /home/heimdall/Desktop/heimdall
# Start all required docker containers
docker-compose up heimdall-backend heimdall-frontend heimdall-proxy heimdall-camera-rtsp
```

### TCP Cameras

The System is able to handle all kinds 

```bash
# Change into the directory where you downloaded heimdall to
cd /home/heimdall/Desktop/heimdall
# Start all required docker containers
docker-compose up heimdall-backend heimdall-frontend heimdall-proxy heimdall-camera-proxy
```

### MQTT Cameras

Connect your MQTT based camera to the provided MQTT Broker (host-ip:1883). Publish images on the channel: `camera`

```bash
# Change into the directory where you downloaded heimdall to
cd /home/heimdall/Desktop/heimdall
# Start all required docker containers
docker-compose up heimdall-backend heimdall-frontend heimdall-proxy
```


## Start Heimdall (using Camera developed at the Bonn-Rhein-Sieg University)

- Camera has a fixed IP adress: `192.168.1.177`
- Commands to get information about Wifi Devices:
  - `nmcli device` # List of Network Devices
  - `nmcli device wifi` # List of Wifi Devices (inkl. )
  - `nmcli device show`
- **Run the commands below - Replace `<wifi_device_id>` with the correct identifier of your wifi card that you want to use**

```sh
sudo apt-get install isc-dhcp-server

sudo nano /etc/default/isc-dhcp-server
    Add <wifi_device_id> to ipv4 interface

sudo nano /etc/dhcp/dhcpd.conf
    subnet 192.168.1.0 netmask 255.255.255.0 {
        range 192.168.1.1 192.168.1.254;
        option subnet-mask 255.255.255.0;
        option routers 192.168.1.177;
        default-lease-time 600;
        max-lease-time 7200;
    }

sudo service isc-dhcp-server restart
```


## Start Heimdall (using the low-energy camera)

```sh
cd /home/heimdall/Desktop/heimdall
sudo nano startHeimdall.sh # replace the WIFI_DEVICE_ID with your wifi hotspot device id and set the WIFI_SSID as well as the WIFI_PASSWORD variable accordingly.
sh startHeimdall.sh # Test installation (make sure everything starts without error messages)
```



## Optional (Not required anymore)

### Disable IPv6

```bash
sudo nano /etc/sysctl.conf

net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1

net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1

sudo sysctl -p # load

cat /proc/sys/net/ipv6/conf/all/disable_ipv6 # check
```

# Useful Commands

## Show connected devices to hotspot

`arp -an`

## Show open ports

`sudo netstat -tulpn`

## Install TeamViewer (on Ubuntu 16.04.3)

```sh
sudo sh installTeamviewer.sh
```

### Install TeamViewer on Ubuntu 17.10

- Set default password
- disable wayland support
  - `sudo nano /etc/gdm3/custom.conf`
  - `WaylandEnable=false`
- Install Dummy Screen
  - `sudo apt-get install xserver-xorg-video-dummy`
  - `sudo nano /usr/share/x11/xorg.conf.d/xorg.conf`
  - https://askubuntu.com/a/463000

## Install Visual Studio Code for Development

- Download [Visual Studio Code from Microsoft Website](https://code.visualstudio.com/)
- `sudo dpkg -i code_1.19.1-1513676564_amd64.deb`
- `sudo apt-get -f install`

## Update the whole project (incl. submodules)

```sh
git pull
git submodule init
git submodule update --recursive --remote
```

## Stop and delete single service

```sh
sudo docker-compose stop heimdall-frontend
sudo docker-compose rm heimdall-frontend
```

## Fix networking issue in Docker (port binding - not used anymore)

```sh
socat TCP-LISTEN:9000,fork TCP:127.0.0.1:9002
socat -d -d tcp4-listen:9000,fork tcp4:127.0.0.1:9002
socat tcp4-listen:9000,fork tcp4:127.0.0.1:9002
```
