# -*- coding: utf-8 -*-
"""
@author: Manuel
"""

import socket
import time
import sys
import json
import sensor_version.config as config
from IoT_Client_functions import read_data_from_sensor
from sensor_version.data_message import message

udp_timeout = 2
udp_delay = 1

if len(sys.argv) != 2:
    print('Error: need client number')
    sys.exit(1)

client_number = int(sys.argv[1])
client_ip = config.arp_table[client_number]

server_address = (config.gateway_UDP_ip, config.gateway_UDP_port)


while True:
    
    print('Reading data from sensor...')
    hour, temperature, humidity = read_data_from_sensor()
    data = message(client_number, hour, temperature, humidity)
    data.set_ip_address(client_ip)
    
    
    OK = False
    while not OK:
        try:
            # socket create
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f'Sending data to {server_address}...')
            data.sending_time(time.time_ns())
            data_bytes = json.dumps(data.__dict__)
            t0 = time.time_ns()
            udp_socket.sendto(data_bytes.encode('utf8'), server_address)
            
            t = time.time_ns()
            dt = t - t0
            print('Socket time:', dt, 'ns')
            print('Waiting for response...')

            udp_socket.settimeout(udp_timeout)

            
            server_response, server = udp_socket.recvfrom(1024)
            if server_response.decode() == 'OK':
                OK = True
            else:
                raise Exception('Wrong Response')
                
        except Exception as error:
            print(f'Error: {error}')
            print('Try sending again...')
            time.sleep(udp_delay)
        
        finally:
            udp_socket.close()
    
    print('Data are correctly sent\n')    

    time.sleep(5)

