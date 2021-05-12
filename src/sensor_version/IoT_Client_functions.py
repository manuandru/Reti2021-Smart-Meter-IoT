# -*- coding: utf-8 -*-
"""
@author: Manuel
"""
import time
import ntptime
import machine
import dht

GTM = 3600
sensor = dht.DHT11(machine.Pin(4))


def read_data_from_sensor():
    sensor.measure()
    (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime()
    datetime = str(hour) + ':' + str(minute)
    temperature = sensor.temperature() # Temperature
    humidity = sensor.humidity() # Humidity
    return (datetime, temperature, humidity)

def set_time(timezone):
    ntptime.settime()
    real_time = time.time() + GTM * timezone
    (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime(real_time)
    machine.RTC().datetime((year, month, mday, 0, hour, minute, second, 0))

