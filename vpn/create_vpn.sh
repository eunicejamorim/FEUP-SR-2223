#!/bin/bash

VPN_SERVER="10.0.5.11:1194"

# - Create and initialize opnevpn (create openvpn config)
docker run -v $PWD/config:/etc/openvpn --rm kylemanna/openvpn ovpn_genconfig -u udp://${VPN_SERVER}

# - Create certificate
docker run -v $PWD/config:/etc/openvpn --rm -it kylemanna/openvpn ovpn_initpki
