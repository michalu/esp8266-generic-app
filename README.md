# esp8266-generic-app
ESP8266 generic application that connects to WIFI and supports bidirectional MQTT communication related to relays, reeds and ds18b20 sensors

# Visual Studio Code extension for ESP8266
VSC Pymakr Preview

# Erase board and deploy new firmware
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