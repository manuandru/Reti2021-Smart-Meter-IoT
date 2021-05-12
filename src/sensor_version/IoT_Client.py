# -*- coding: utf-8 -*-
"""
@author: Manuel
"""

import socket
import time
import json
import network
from data_message import message
import IoT_Client_functions
import config


udp_timeout = 2     # timeout time for waiting response from gateway
udp_delay = 1       # delay between two connection to
client_number = 1   # number for identifing clients

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.ifconfig((config.client_UDP_ip, config.client_UDP_subnet, config.network_client_ip, config.DNS_ip))
    sta_if.connect(config.wifi_ssid, config.wifi_password)
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())

IoT_Client_functions.set_time(2) # my function to adjust time accorting to NTP and timezone

print(time.time())


server_address = (config.gateway_UDP_ip, config.gateway_UDP_port)

while True:
    
    print('Reading data from sensor...')
    hour, temperature, humidity = IoT_Client_functions.read_data_from_sensor()
    data = message(client_number, hour, temperature, humidity)
    
    
    OK = False
    while not OK:
        try:
            # socket create
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Sending data to ' + server_address[0] + '...')
            data.sending_time(time.time_ns())
            data_bytes = json.dumps(data.__dict__)
            udp_socket.sendto(data_bytes.encode('utf8'), server_address)
            
            print('Waiting for response...')
            udp_socket.settimeout(udp_timeout)

            
            server_response, server = udp_socket.recvfrom(1024)
            if server_response.decode() == 'OK':
                OK = True
            else:
                raise Exception('Wrong Response')
                
        except Exception as error:
            print('Error: ' + str(error))
            print('Try sending again...')
            time.sleep(udp_delay)
        
        finally:
            udp_socket.close()
    
    print('Data are correctly sent\n')    

    time.sleep(5)
