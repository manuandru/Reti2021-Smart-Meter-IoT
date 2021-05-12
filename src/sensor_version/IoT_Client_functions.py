# -*- coding: utf-8 -*-
"""
@author: Manuel
"""
import time
import ntptime
import machine

GTM = 3600

reading_waiting_time = 0

def read_data_from_sensor():
    hour = '10:00' # Hour
    temperature = '18.00' # Temperature
    humidity = '75.00' # Humidity
    time.sleep(reading_waiting_time)
    return (hour, temperature, humidity)

def set_time(timezone):
    ntptime.settime()
    real_time = time.time() + GTM * timezone
    (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime(real_time)
    machine.RTC().datetime((year, month, mday, 0, hour, minute, second, 0))

