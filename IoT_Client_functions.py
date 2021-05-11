# -*- coding: utf-8 -*-
"""
@author: Manuel
"""
import time

reading_waiting_time = 0

def read_data_from_sensor():
    hour = '10:00' # Hour
    temperature = '18.00' # Temperature
    humidity = '75.00' # Humidity
    time.sleep(reading_waiting_time)
    return (hour, temperature, humidity)
