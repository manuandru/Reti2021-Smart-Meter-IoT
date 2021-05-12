# -*- coding: utf-8 -*-
"""
@author: Manuel
"""

import socket
import time
import config
import pickle

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (config.gateway_UDP_ip, config.gateway_UDP_port)

udp_socket.bind(server_address)

while True:
    clients = dict()
    
    ready = False
    # loop until all devices have sent their data
    while not ready:
        print('Waiting for data...')
        
        data_bytes, address = udp_socket.recvfrom(1024)
        
        data = pickle.loads(data_bytes)
        data.arriving_time(time.time_ns()) # add arriving packet time
        data.ip_address(address[0]) # add sender address information
        
        # Store data if not already done
        if data.client not in clients:
            clients[data.client] = data
            print(f'Client {data.client} data is arrived')
    
        
        if data:
            udp_socket.sendto('OK'.encode('utf8'), address)
            #print('Sending check message\n')
        
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
        
        clients_bytes = pickle.dumps(clients, protocol=pickle.HIGHEST_PROTOCOL)
        tcp_socket.send(clients_bytes)
        time.sleep(1)
        tcp_socket.close()
        sent = True
    
    print('Data is correctly sent to the server\n')
    time.sleep(2)

    
        