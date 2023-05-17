#!/bin/bash

CLIENT=client

# - Create client account
docker run -v $PWD/config:/etc/openvpn --rm -it kylemanna/openvpn easyrsa build-client-full ${CLIENT} nopass

# - Copy client certificate (ovpn file) from container
docker run -v $PWD/config:/etc/openvpn --rm kylemanna/openvpn ovpn_getclient ${CLIENT} > ${CLIENT}.ovpn