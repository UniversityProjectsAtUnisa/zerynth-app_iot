import adc
import timers
import config as cfg

# Definizione dell'ascoltatore
class Listener:
    # Configurato tramite parametri nel file config
    def __init__(self, soundSensorPin):
        self.sndSnsr = soundSensorPin
        
    # Metodo di singolo ascolto
    def listen(self):
        sensorValue = adc.read(self.sndSnsr)
    
        if sensorValue < cfg.THRESHOLD:
            return False
            
        # La prima volta supera il THRESHOLD
        print("Primo")
        t = timers.timer()
        t.start()
        sleep(cfg.DEBOUNCE)
        
        
        # Poi non supera più il THRESHOLD per un tempo INTERVAL
        while(t.get() < cfg.INTERVAL):
            sensorValue = adc.read(self.sndSnsr)
            if sensorValue > cfg.THRESHOLD:
                print("Troppo presto")
                return False
            sleep(cfg.SCAN_PERIOD)
            
        t.reset()
        # Poi supera il THRESHOLD in un tempo INTERVAL
        while(t.get() < cfg.INTERVAL):
            sensorValue = adc.read(self.sndSnsr)
            if sensorValue > cfg.THRESHOLD:
                return True
            sleep(cfg.SCAN_PERIOD)
        
        print("Troppo tardi")
        return False