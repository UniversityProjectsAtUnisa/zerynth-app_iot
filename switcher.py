import pwm
import config as cfg

class Switcher:
    PWM_PERIOD = cfg.PWM_PERIOD
    def __init__(self, ledPin, buzzer):
        self.buzzer = buzzer
        self.led = ledPin
        self.ledState = LOW
        
    def on_change(self, callback):
        self.publish_leds_state = callback
        
    def switch(self, message = ''):
        print(message)
        if self.ledState == LOW:
            self.ledState = HIGH
            digitalWrite(self.led, HIGH)
            self.buzzer.playTurnOn()
        else:
            self.ledState = LOW
            digitalWrite(self.led, LOW)
            self.buzzer.playTurnOff()
        self.publish_leds_state()
        
    def set(self, mqttPayload):
        l = int(mqttPayload)
        if l > 0:
            self.ledState = HIGH
            digitalWrite(self.led, HIGH)
            self.buzzer.playTurnOn()
        else:
            self.ledState = LOW
            digitalWrite(self.led, LOW)
            self.buzzer.playTurnOff()
        self.publish_leds_state()