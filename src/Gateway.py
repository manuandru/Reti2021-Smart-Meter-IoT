# -*- coding: utf-8 -*-
"""
@author: Manuel
"""

import socket
import time
import sensor_version.config as config
import json
import pickle
from sensor_version.data_message import message

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (config.gateway_UDP_ip, config.gateway_UDP_port)

udp_socket.bind(server_address)

while True:
    clients = dict()
    
    ready = False
    # loop until all devices have sent their data
    while not ready:
        print('Waiting for data...')
        
        data_bytes, address = udp_socket.recvfrom(4096)
        
        data = json.loads(data_bytes.decode())
        data = message(**data)
        data.arriving_time(time.time_ns()) # add arriving packet time
        data.set_ip_address(address[0]) # add sender address information
        
        # Store data if not already done
        if data.client not in clients:
            clients[data.client] = data
            print(f'Client {data.client} data is arrived')
    
        
        if data:
            udp_socket.sendto('OK'.encode('utf8'), address)
        
        if len(clients) == config.number_of_clients:
            ready = True
    
    print('All clients have sent. Sending to server...')
    
    sent = False
    while not sent:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            tcp_socket.connect((config.server_TCP_ip, config.server_TCP_port))
        except Exception as error:
            print(f'Error: {error}')
            print('Trying again...')
            time.sleep(2)
            continue
        
        clients_bytes = pickle.dumps(clients)
        t0 = time.time_ns()
        tcp_socket.send(clients_bytes)
        t = time.time_ns()
        tcp_socket.close()
        sent = True
        dt = t - t0
    
    print(f'Data is correctly sent to the server in {dt/10e6}\n')
    time.sleep(2)

    
        