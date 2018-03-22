#! /bin/sh

if [ `whoami` != root ]; then
    echo Please run this script as root or using sudo
    exit
fi

# Stop/Disable Bluetooth (not needed)
systemctl stop bluetooth.service
systemctl disable bluetooth.service
service bluetooth status

# Go to heimdall location
cd ~/Desktop/heimdall

# Read config
export `cat env.vars`

echo $WIFI_DEVICE_ID
echo $WIFI_SSID
echo $WIFI_PASSWORD

# Setup WiFi
echo "___________"
echo "Setup Wifi - Using Device: $WIFI_DEVICE_ID"
# Get List of Network Devices:
# nmcli device
# nmcli device wifi
nmcli device wifi hotspot ifname "$WIFI_DEVICE_ID" con-name "$WIFI_SSID" ssid "$WIFI_SSID" band bg password "$WIFI_PASSWORD"
# nmcli device wifi connect <ssid> password <password> ifname 'wlp2s0'


# Set IP-Adress
echo "\r\n___________\r\nSet IP Address"
ifconfig "$WIFI_DEVICE_ID" 192.168.1.177 netmask 255.255.255.0


echo "\r\n___________\r\nRestart DHCP-Server"
service isc-dhcp-server restart

echo "\r\n___________\r\nRecreating bridge network for camera"

# Since the default network bridge network create by docker does not have a proper IPv4 Binding, the camera can't access it via the Hotspot
docker network rm bridge-iot
docker network create -o "com.docker.network.bridge.host_binding_ipv4"="192.168.1.177" bridge-iot

echo "\r\n___________\r\nStarting docker container.."
docker-compose up heimdall-backend heimdall-frontend heimdall-proxy heimdall-camera-proxy
