# -*- coding: utf-8 -*-
"""
@author: Manuel
"""

class message:

    def __init__(self, client, hour, temperature, humidity, t0 = None, t = None, ip_address = None):
        self.client = client
        self.hour = hour
        self.temperature = temperature
        self.humidity = humidity
        self.t0 = t0
        self.t = t
        self.ip_address = ip_address
    
    def sending_time(self, t0):
        self.t0 = t0
    
    def arriving_time(self, t):
        self.t = t

    def travelling_time(self):
        return self.t - self.t0
    
    def set_ip_address(self, ip_address):
        self.ip_address = ip_address