# Imposto i parametri di riconoscimento del comando di commutazione
THRESHOLD = 1750
SCAN_PERIOD = 25
DEBOUNCE = 4 * SCAN_PERIOD
INTERVAL = 14 * SCAN_PERIOD

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

        
    def changeMode(self):
        print("Premuto bottone onBoard")
        self.en = not (self.en and self.muted)
        self.muted = not (self.en and self.muted) 
        digitalWrite(self.enabledLed, HIGH if self.en else LOW)
        digitalWrite(self.mutedLed, HIGH if self.muted else LOW)