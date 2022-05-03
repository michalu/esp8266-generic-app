import network
import time
import ubinascii

def connect(config: dict):
    '''Connects to wireless network using parameters specified in cfg.py file WIFI section
    '''
    station = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF)

    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print ('MAC address: ' + mac)

    #turn off access point
    ap.active(False)

    station.active(True)
    station.connect(config["ssid"], config["password"])

    while station.isconnected() == False:
        print("Connecting ...")
        time.sleep_ms(1000)

    print('Connection successful')
    print(station.ifconfig())