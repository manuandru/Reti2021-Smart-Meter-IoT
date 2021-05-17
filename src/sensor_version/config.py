# -*- coding: utf-8 -*-
"""
@author: Manuel
"""

number_of_clients = 4 # To wait for transmit message to the Server

# WI-FI setup
wifi_ssid = 'ssid'
wifi_password = 'password'

# Simulation ARP table
arp_table = {
    1 : '192.168.1.20',
    2 : '192.168.1.25',
    3 : '192.168.1.30',
    4 : '192.168.1.35',
}


# Real network information
client_UDP_subnet = '255.255.255.0'
network_client_ip = '192.168.1.1'
DNS_ip = '8.8.8.8'

# Gateway network information
gateway_UDP_ip = '192.168.1.10'
gateway_UDP_port = 10000

# Server network information
server_TCP_ip = 'localhost' # 10.10.10.2/24
server_TCP_port = 2000
