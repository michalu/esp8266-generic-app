import cfg
import wifi
import mqtt
import onewire
import ds18x20
from machine import Pin

def init(cfg: dict):
    '''Reads configuration from cfg.py
    initiates PINS (relay, trigger, reed, temp) according to configuration
    '''
    for pin in cfg.PINS:
        p = cfg.PINS[pin]
        if p['type'] == "relay":
            p["obj"] = Pin(p["gpio"], Pin.OUT)
            p["obj"].value(1)
            print("relay created: " + pin)
        elif p['type'] == "trigger":
            p["obj"] = Pin(p["gpio"], Pin.OUT)
            p["obj"].value(1)
            print("trigger created: " + pin)
        elif p['type'] == "reed":
            p["obj"] = Pin(p["gpio"], Pin.IN, Pin.PULL_UP)
            print("reed created: " + pin)
        elif p['type'] == "temp":
            dat = Pin(p["gpio"])
            ow = onewire.OneWire(dat)
            p["obj"] = ds18x20.DS18X20(ow)
            p["roms"] = p["obj"].scan()
            for rom in p["roms"]:
                serialnum = hex(int.from_bytes(rom, 'little'))
                print('temp created:', serialnum)
    return cfg.PINS

pins = init(cfg)

wifi.connect(cfg.WIFI)

mqtt.connect(cfg, pins)