FROM danchitnis/xrdp:ubuntu-xfce
RUN apt update && apt install software-properties-common -y
RUN sudo add-apt-repository ppa:mozillateam/ppa
RUN apt update && apt install iproute2 iputils-ping tcpdump iptables dnsutils curl apache2-utils nano remmina openssh-server openvpn firefox-esr -y
COPY ./random_files /random_files