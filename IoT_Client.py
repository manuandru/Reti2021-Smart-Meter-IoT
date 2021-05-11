# -*- coding: utf-8 -*-
"""
@author: Manuel
"""

import socket
import time
import sys
import config
from IoT_Client_functions import read_data_from_sensor
import pickle
from data_message import message

udp_timeout = 2
udp_delay = 1

if len(sys.argv) != 2:
    print('Error: need client number')
    sys.exit(1)

client_number = int(sys.argv[1])

server_address = (config.gateway_UDP_ip, config.gateway_UDP_port)


while True:
    
    print('Reading data from sensor...')
    hour, temperature, humidity = read_data_from_sensor()
    data = message(client_number, hour, temperature, humidity)
    
    
    OK = False
    while not OK:
        try:
            # socket create
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f'Sending data to {server_address}...')
            data.sending_time(time.time_ns())
            data_bytes = pickle.dumps(data)
            udp_socket.sendto(data_bytes, server_address)
            
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

