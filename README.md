# esp8266-generic-app
This is an ESP8266 generic application that connects to WIFI and supports bidirectional MQTT communication related to relays, reeds and ds18b20 sensors that are connected to this board.

Application allows to:
- control relays (turn on, turn off) by a message send to the input queue,
- trigger relays (useful for opening/closing gates that are triggered by providing voltage for short period of time) by a message send to the input queue,
- get relays, ds18b20 sensors and reeds state by a message published by this app and received  the from output queue.

# Visual Studio Code extension for ESP8266
Pymakr Preview - VSC extension is easy to use and supports uploading/downloading files and running apps.

# How to deploy new firmware
Erase:
```
esptool.py --port /dev/tty.usbserial-0001 erase_flash
```
Deploy new firmware:
```
esptool.py --port /dev/tty.usbserial-0001 --baud 460800 write_flash --flash_size=detect 0 firmware/esp8266-1m-20220117-v1.18.bin
```

# Running MQTT Broker as docker container
Mosquitto
```
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto
```