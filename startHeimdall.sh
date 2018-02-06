#! /bin/sh

if [ `whoami` != root ]; then
    echo Please run this script as root or using sudo
    exit
fi

WIFI_DEVICE_ID="wlx8416f9176c99"
WIFI_SSID="ssid"
WIFI_PASSWORD="password"

echo "___________"
echo "Setup Wifi - Using Device: $WIFI_DEVICE_ID"
# Get List of Network Devices:
# nmcli device
# nmcli device wifi
nmcli device wifi hotspot ifname "$WIFI_DEVICE_ID" con-name "$WIFI_SSID" ssid "$WIFI_SSID" band bg password "$WIFI_PASSWORD"
# nmcli device wifi connect <ssid> password <password> ifname 'wlp2s0'


echo " "
echo "___________"
echo "Set IP Address"
ifconfig "$WIFI_DEVICE_ID" 192.168.1.177 netmask 255.255.255.0


echo " "
echo "___________"
echo "Restart DHCP-Server"
service isc-dhcp-server restart

echo " "
echo "___________"
echo "Recreating bridge network for camera"

# Since the default network bridge network create by docker does not have a proper IPv4 Binding, the camera can't access it via the Hotspot
docker network rm bridge-iot
docker network create -o "com.docker.network.bridge.host_binding_ipv4"="192.168.1.177" bridge-iot

echo " "
echo "___________"
echo "Starting docker container.. "
cd /home/heimdall/Desktop/heimdall
docker-compose up heimdall-backend heimdall-frontend heimdall-proxy heimdall-camera-proxy
