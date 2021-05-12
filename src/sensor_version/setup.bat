set port=COM6

ampy -p %port% rm /config.py
ampy -p %port% rm /data_message.py
ampy -p %port% rm /main.py
ampy -p %port% rm /IoT_Client_functions.py

ampy -p %port% put IoT_Client_functions.py
ampy -p %port% put config.py
ampy -p %port% put data_message.py
ampy -p %port% put IoT_Client.py /main.py