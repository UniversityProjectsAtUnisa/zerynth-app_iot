# Imposto i parametri di riconoscimento del comando di commutazione
HIGH_THRESHOLD = 3000
LOW_THRESHOLD = 300
SCAN_PERIOD = 1

CYCLES_STEP_1 = 10
SLEEP_STEP_1 = 10
CYCLES_STEP_2 = 300
SLEEP_STEP_2 = 1

DEBOUNCE = 100 * SCAN_PERIOD
INTERVAL = 250 * SCAN_PERIOD
MAX_LUX_DETECTED = 50000
PWM_PERIOD = 10000

class ModeHandler:
    def __init__(self, enabledLedPin, mutedLedPin):
        # Enabled
        self.en = True
        self.enabledLed = enabledLedPin
        digitalWrite(self.enabledLed, HIGH)
        # Muted
        self.muted = False
        self.mutedLed = mutedLedPin
        digitalWrite(self.mutedLed, LOW)
        
    def on_change(self, callback):
        self.publish_leds_state = callback

        
    def changeMode(self):
        print("Premuto bottone onBoard")
        self.en = not (self.en and self.muted)
        self.muted = not (self.en and self.muted) 
        digitalWrite(self.enabledLed, HIGH if self.en else LOW)
        digitalWrite(self.mutedLed, HIGH if self.muted else LOW)
        self.publish_leds_state()
        
    def set(self, mqttPayload):
        e, m = [int(x) for x in mqttPayload.split(' ')]
        self.en = True if e > 0 else False
        self.muted = True if m > 0 else False
        digitalWrite(self.enabledLed, HIGH if self.en else LOW)
        digitalWrite(self.mutedLed, HIGH if self.muted else LOW)
        self.publish_leds_state()