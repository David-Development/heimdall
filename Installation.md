# Setup

- System was tested on XUbuntu 16.04.3

## Setup Camera (developed at the Bonn-Rhein-Sieg University)

- Camera has a fixed IP adress: `192.168.1.177`
- Commands to get information about Wifi Devices:
  - `nmcli device` # List of Network Devices
  - `nmcli device wifi` # List of Wifi Devices (inkl. )
  - `nmcli device show`
- **Run the commands below - Replace `<wifi_device_id>` with the correct wifi device id**

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

## Clone this repo

```sh
cd /home/heimdall/Desktop
git clone --recursive https://github.com/David-Development/heimdall.git
```

## Install Docker & Docker Compose

- Run `installDocker.sh` file from the root of the heimdall project or follow the installation instructions on [docs.docker.com](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository)

## Pull Heimdall Docker Images

```sh
docker pull luhmer/opencv-python3
docker pull luhmer/heimdall-backend
docker pull luhmer/heimdall-frontend
```

## Installation of Heimdall

```sh
cd /home/heimdall/Desktop/heimdall
sudo nano startHeimdall.sh # replace the WIFI_DEVICE_ID with your wifi hotspot device id and set the WIFI_SSID as well as the WIFI_PASSWORD variable accordingly.
sh startHeimdall.sh # Test installation (make sure everything starts without error messages)
```

### Setup Heimdall to start while booting

- `sudo nano /etc/rc.local`
- Append the following code snippet (before the `exit 0` line)

```sh
sh /home/heimdall/Desktop/heimdall/startHeimdall.sh > /home/heimdall/Desktop/heimdall-log.txt 2>&1 &
exit 0
```

#### Access log file

`tail -f -n 100 heimdall-log.txt`


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