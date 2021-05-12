# -*- coding: utf-8 -*-
"""
@author: Manuel
"""

import socket
import pickle
import sensor_version.config as config

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (config.server_TCP_ip, config.server_TCP_port)
tcp_socket.bind(server_address)
tcp_socket.listen(1)

print(f'The server is up on {server_address[0]}:{server_address[1]}')

while True:
    
    print ('Ready to serve...')
    connectionSocket, addr = tcp_socket.accept()

    try:
        data_bytes = connectionSocket.recv(1024)
        data = pickle.loads(data_bytes)
        connectionSocket.close()

    except IOError as error:
        print(f'Error: {error}')
    
    for k, v in sorted(data.items()):
        print(f'{v.ip_address} - {v.hour}h - {v.temperature}°C - {v.humidity}%')
