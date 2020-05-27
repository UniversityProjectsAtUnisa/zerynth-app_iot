import buzzerFeedback as bfb
import config as cfg

class Switcher:
    def __init__(self, buzzerPin, ledPin, modeHandler):
        # Inizializzo il buzzer
        self.buzzer = bfb.Buzzer(buzzerPin, modeHandler)
        self.led = ledPin
        self.ledState = LOW
        
    def switch(self, message = ''):
        print(message)
        if self.ledState == LOW:
            self.ledState = HIGH
            digitalWrite(self.led, self.ledState)
            self.buzzer.playTurnOn()
        else:
            self.ledState = LOW
            digitalWrite(self.led, self.ledState)
            self.buzzer.playTurnOff()
        sleep(cfg.INTERVAL)
        
    def set(self, mqttPayload):
        print(mqttPayload)
        l = int(mqttPayload)
        if l > 0:
            self.ledState = HIGH
            digitalWrite(self.led, self.ledState)
            self.buzzer.playTurnOn()
        else:
            self.ledState = LOW
            digitalWrite(self.led, self.ledState)
            self.buzzer.playTurnOff()