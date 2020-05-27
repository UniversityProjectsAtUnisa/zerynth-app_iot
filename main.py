# ClapToLightUp
# Created at 2020-05-25 14:43:55.054532

import streams
import checkDoubleClap as cdc
import switcher as swc
import config as cfg
import timers

from mqtt import mqtt
from espressif.esp32net import esp32wifi as wifi_driver
from wireless import wifi
wifi_driver.auto_init()

# Apertura stream seriale
streams.serial()

# Imposto il sensore di suono per la lettura analogica
sndSnsrPin = A4
pinMode(sndSnsrPin, INPUT_ANALOG)

# Imposto il led principale per la scrittura digitale
mainLedPin = D23
pinMode(mainLedPin, OUTPUT)

# Imposto i led di stato
enabledLedPin = D19
pinMode(enabledLedPin, OUTPUT)
mutedLedPin = D5
pinMode(mutedLedPin, OUTPUT)

# Imposto il button integrato per il cambio di modalità
modeButtonPin = BTN0
pinMode(modeButtonPin, INPUT_PULLUP)

# Inizializzo un ModeHandler
modeHandler = cfg.ModeHandler(enabledLedPin, mutedLedPin)

# Imposto il buzzer per funzionare in pwm
buzzerPin = D18.PWM
pinMode(buzzerPin, OUTPUT)

# Imposto il button per l'accensione manuale del led
lightButtonPin = D12
pinMode(lightButtonPin,INPUT_PULLDOWN)

# Inizializzo un Listener
listener = cdc.Listener(sndSnsrPin)

# Inizializzo uno Switcher
switcher = swc.Switcher(buzzerPin, mainLedPin, modeHandler)


# Alla pressione del bottone integrato cambio la modalità
onPinFall(modeButtonPin, modeHandler.changeMode)

# Alla pressione del bottone cambio lo stato del led principale
onPinFall(lightButtonPin, switcher.switch, "Dal Bottone")


print("Establishing Link...")
try:
    wifi.link("Della Rocca",wifi.WIFI_WPA2,"xDrxQjn7b7")
except Exception as e:
    print("ooops, something wrong while linking :(", e)
    while True:
        sleep(1000)


def publish_leds_state():
    client.publish("current/leds", 
    ('1 ' if switcher.ledState else '0 ') + 
    ('1 ' if modeHandler.en    else '0 ') +
    ('1'  if modeHandler.muted else '0' )
    )
    
    
# define MQTT callbacks
def on_message(client, data):
    message = data['message']
    print('message.topic')
    if message.topic == 'new/luce':
        switcher.set(message.payload)
    elif message.topic == 'new/mode':
        modeHandler.set(message.payload)
    elif message.topic == 'new/change':
        modeHandler.changeMode()
    publish_leds_state()
    
    

try:
    client = mqtt.Client("zerynth-mqtt",True)
    for retry in range(10):
        try:
            client.connect("test.mosquitto.org", 60)
            break
        except Exception as e:
            print("connecting...")
    print("connected.")
    # subscribe to channels
    client.subscribe([["new/+", 1]])
    
    # start the mqtt loop
    client.loop(on_message)
    
    t=timers.timer()
    t.interval(5000, publish_leds_state)
    
    
    
    
    print("Starting loop")

    while(True):
        # Se il Listener rileva un segnale di commutazione, commuto lo stato del led tramite lo switcher
        if modeHandler.en and listener.listen():
            switcher.switch("Dal Suono")
            
        sleep(cfg.SCAN_PERIOD)
except Exception as e:
    print(e)