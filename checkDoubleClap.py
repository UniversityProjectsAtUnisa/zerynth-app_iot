import adc
import timers
import config as cfg

# Definizione dell'ascoltatore
class Listener:
    def __init__(self, soundSensorPin, potentiometerPin):
        self.sndSnsr = soundSensorPin
        self.potentiometer = potentiometerPin
        
    def readSound(self):
        sound = adc.read(self.sndSnsr)
        multiplier = adc.read(self.potentiometer) / 1500.0 # Al posto di 4095.0 per usare il potenziometro in posizione centrale
        return sound * multiplier
        
    # Metodo di singolo ascolto
    def listen(self):
        step = 0
        
        if step == 0:
            sensorValue = self.readSound()
            if sensorValue > cfg.HIGH_THRESHOLD:
                step = 1
        
        if step == 1:
            print("PRIMO")
            for _ in range(cfg.CYCLES_STEP_1):
                sleep(cfg.SLEEP_STEP_1)
                sensorValue = self.readSound()
                if sensorValue < cfg.LOW_THRESHOLD:
                    step = 2
        
        if step == 2:
            for _ in range(cfg.CYCLES_STEP_2):
                sleep(cfg.SLEEP_STEP_2)
                sensorValue = self.readSound()
                if sensorValue > cfg.HIGH_THRESHOLD:
                    sleep(cfg.DEBOUNCE)
                    return True
                    
        return False