# ClapToLightUp
# Created at 2020-05-25 14:43:55.054532

import streams
import checkDoubleClap as cdc
import switcher as swc
import light_driver as ld
import config as cfg
import timers

import internet

# Apertura stream seriale
streams.serial()

# Imposto il sensore di suono per la lettura analogica
sndSnsrPin = A0
pinMode(sndSnsrPin, INPUT_ANALOG)

# Imposto il led principale per la scrittura digitale
mainLedPin = D23.PWM
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
buzzerPin = D12.PWM
pinMode(buzzerPin, OUTPUT)

# Imposto il button per l'accensione manuale del led
lightButtonPin = D14
pinMode(lightButtonPin,INPUT_PULLDOWN)

# Imposto un potenziometro per la regolazione della sensibilità del sistema
potentiometerPin = A4
pinMode(potentiometerPin,INPUT_ANALOG)

# Inizializzo un Listener
listener = cdc.Listener(sndSnsrPin, potentiometerPin)

# Inizializzo uno Switcher
switcher = swc.Switcher(buzzerPin, mainLedPin, modeHandler)


# Alla pressione del bottone integrato cambio la modalità
onPinFall(modeButtonPin, modeHandler.changeMode)

# Alla pressione del bottone cambio lo stato del led principale
onPinFall(lightButtonPin, switcher.switch, "Dal Bottone")

# Mi collego al wifi
internet.connect()


# Inizializzo il lightSensor
lightSensor = ld.LightSensor(I2C0)

def measure_light():
    brighnessPercentage = lightSensor.measure_high_res()
    publish_light(brighnessPercentage)
    switcher.setDutyCycle(brighnessPercentage)
    

def publish_light(brighnessPercentage):
    message = str(brighnessPercentage)
    try:
        client.publish("current/light", message)
        print(message)
    except Exception as e:
        print('publish_leds_state failed for message: ', message)

def publish_leds_state():
    message = ""
    message += ('1 ' if switcher.ledState else '0 ') 
    message += ('1 ' if modeHandler.en    else '0 ')
    message += ('1'  if modeHandler.muted else '0' )
        
    try:
        client.publish("current/leds", message, retain=True)
        print(message)
    except Exception as e:
        print('publish_leds_state failed for message: ', message)
    
    
modeHandler.on_change(publish_leds_state)
switcher.on_change(publish_leds_state)
    
    
# define MQTT callbacks
def on_message(client, data):
    message = data['message']
    print(message.topic)
    if message.topic == 'new/luce':
        switcher.set(message.payload)
    elif message.topic == 'new/mode':
        modeHandler.set(message.payload)
    elif message.topic == 'new/change':
        modeHandler.changeMode()
    
    
try:
    client = internet.Client("zerynth-mqtt-marco741")
    
    # subscribe to channels
    client.subscribe([["new/+", 1]])
    
    # start the mqtt loop
    client.loop(on_message)
    
    publish_leds_state()
    t = timers.timer()
    t.interval(1500, measure_light)
    
    
    
    
    print("Starting loop")

    while(True):
        # Se il Listener rileva un segnale di commutazione, commuto lo stato del led tramite lo switcher
        if modeHandler.en and listener.listen():
            switcher.switch("Dal Suono")
            
        sleep(cfg.SCAN_PERIOD)
except Exception as e:
    print(e)
    
    
    
