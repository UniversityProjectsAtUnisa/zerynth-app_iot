# ClapToLightUp
# Created at 2020-05-25 14:43:55.054532

import streams
import checkDoubleClap as cdc
import switcher as swc
import config as cfg

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





print("Starting loop")
while(True):
    # Se il Listener rileva un segnale di commutazione, commuto lo stato del led tramite lo switcher
    if modeHandler.en and listener.listen():
        switcher.switch("Dal Suono")
        
    sleep(cfg.SCAN_PERIOD)
