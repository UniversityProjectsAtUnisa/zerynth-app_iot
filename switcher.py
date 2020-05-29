import pwm
import config as cfg

class Switcher:
    PWM_PERIOD = cfg.PWM_PERIOD
    def __init__(self, ledPin, buzzer):
        self.buzzer = buzzer
        self.led = ledPin
        self.ledState = LOW
        self.dutyCycle = 0.5
        
    def on_change(self, callback):
        self.publish_leds_state = callback
        
    def switch(self, message = ''):
        print(message)
        if self.ledState == LOW:
            self.ledState = HIGH
            self.writePwm()
            self.buzzer.playTurnOn()
        else:
            self.ledState = LOW
            self.writePwm()
            self.buzzer.playTurnOff()
        self.publish_leds_state()
        
    def set(self, mqttPayload):
        l = int(mqttPayload)
        if l > 0:
            self.ledState = HIGH
            self.writePwm()
            self.buzzer.playTurnOn()
        else:
            self.ledState = LOW
            self.writePwm()
            self.buzzer.playTurnOff()
        self.publish_leds_state()
        
    def writePwm(self):
        if self.ledState == HIGH:
            pwm.write(self.led, self.PWM_PERIOD, int(self.PWM_PERIOD*self.dutyCycle), MICROS)
        else:
            pwm.write(self.led, 0, 0, MICROS)
        
    def setDutyCycle(self, brightnessPercentage):
        self.dutyCycle = 1 - brightnessPercentage/100
        self.writePwm()