import time
import machine
from umqttsimple import MQTTClient
import time
import ubinascii
import json

client = None
pins = None
config = None

def sub_cb(topic: str, msg: str):
    '''Handler for incoming MQTT messages - allows to switch relays
    '''
    try:
        #Sample msg: {"P1": 1, "P2": 0} - applies only to pins in cfg.py where type="relay"
        data = json.loads(msg)
        send = False
        for pin in data:
            v = 1 - data[pin]
            p = pins[pin]
            if p["type"] == "relay":
                if p['obj'].value() != v:
                    p['obj'].value(v)
                    send = True
        if send:
            time.sleep_ms(1000)
            #Immediate response 
            state = get_state(pins)
            client.publish(config.MQTT["queue_out"], state)
    except Exception as e:
        print(e)

def restart_and_reconnect():
    '''In case there are any problems with MQTT connection we reboot
    '''
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

def get_state(pins: dict):
    '''Goes through the pins and prepares output message to be send to MQTT server
    '''
    result = {}
    for pin in pins:
        p = pins[pin]
        if p['type'] == "reed":
            v = 1 - p['obj'].value()
            result[pin] = v
        elif p['type'] == "relay":
            v = 1 - p['obj'].value()
            result[pin] = v
        elif p['type'] == "temp":
            p['obj'].convert_temp()
            time.sleep_ms(750)
            v = 0
            result[pin] = {}
            for rom in p['roms']:
                v = p['obj'].read_temp(rom)
                serialnum = hex(int.from_bytes(rom, 'little'))
                result[pin][serialnum] = v
    state = json.dumps(result)
    return state

def connect(cfg: dict, apins: dict):
    '''Connects to MQTT server and subscribes to the topic queue_in configured in cfg.py
    '''
    global client
    global pins
    global config

    config = cfg
    config_mqtt = config.MQTT
    pins = apins

    client_id = ubinascii.hexlify(machine.unique_id())

    try:
        print("Connecting to MQTT broker ...")
        client = MQTTClient(client_id, server=config_mqtt["server"], user=config_mqtt["user"], password=config_mqtt["pwd"], port=config_mqtt["port"])
        client.set_callback(sub_cb)
        client.connect()
        client.subscribe(config_mqtt["queue_in"])
        print('Connected to %s MQTT broker, subscribed to %s topic' % (config_mqtt["server"], config_mqtt["queue_in"]))
    except OSError as e:
        print(e)
        restart_and_reconnect()

    #main loop for receiving messages from queue_in and sending notifications to queue_out
    prevstate = None
    last_message = 0
    while True:
        try:
            client.check_msg()
            #get current state
            state = get_state(pins)
            #send notifications about changes only if there is some change in the state
            if state != prevstate:
                #send notification every interval (defined in seconds in cfg.py)
                #to avoid too frequent notifications
                if (time.time() - last_message) > config_mqtt["interval"]:
                    client.publish(config_mqtt["queue_out"], state)
                    prevstate = state
                    last_message = time.time()

        except OSError as e:
            print(e)
            restart_and_reconnect()