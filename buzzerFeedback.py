import pwm

LOW_NOTE_FREQUENCY = 466
HIGH_NOTE_FREQUENCY = 622

class Buzzer:
    
    # In microsecondi, come intero
    lowNotePeriod = 1000000//LOW_NOTE_FREQUENCY
    highNotePeriod =  1000000//HIGH_NOTE_FREQUENCY
    
    def __init__(self, buzzerPin, modeHandler):
        self.buzzerPin = buzzerPin
        self.modeHandler = modeHandler
        
    
    # Suono all'accensione del led
    def playTurnOn(self):
        print("Low -> High: ", LOW_NOTE_FREQUENCY, HIGH_NOTE_FREQUENCY)
        
        
        # Imposto il poeriodo del buzzer ed il duty cycle a 50%
        if not self.modeHandler.muted:
            p = self.lowNotePeriod
            pwm.write(self.buzzerPin, p, p//2, MICROS)
            
        sleep(200) 
        
        if not self.modeHandler.muted:
            p = self.highNotePeriod
            pwm.write(self.buzzerPin, p, p//2, MICROS)
        sleep(300)
        
        pwm.write(self.buzzerPin, 0, 0, MICROS)
        
    
    # Suono allo spegnimento del led
    def playTurnOff(self):
        print("High -> Low: ", HIGH_NOTE_FREQUENCY, LOW_NOTE_FREQUENCY)
        
        
        if not self.modeHandler.muted:
            p = self.highNotePeriod
            pwm.write(self.buzzerPin, p, p//2, MICROS)
        
        sleep(200) 
        
        
        if not self.modeHandler.muted:
            p = self.lowNotePeriod
            pwm.write(self.buzzerPin, p, p//2, MICROS)
        sleep(300)
        
        pwm.write(self.buzzerPin, 0, 0, MICROS)
        