import pwm
import threading

LOW_NOTE_FREQUENCY = 466 # Bb
HIGH_NOTE_FREQUENCY = 622 # Eb

TEMPO = 120 # bpm

_E4 = 1000000// 330
_G4 = 1000000// 392
_A4 = 1000000// 440
_Ad4= 1000000// 466
_B4 = 1000000// 494
_C5 = 1000000// 523
_Cd5= 1000000// 554
_D5 = 1000000// 587
_E5 = 1000000// 659
_Fd5= 1000000// 698
_G5 = 1000000// 784
_A5 = 1000000// 880
_B5 = 1000000// 988
_D6 = 1000000// 1175

# Don't start now - Dua Lipa (BassLine)
musicSheets = [
    (_E4, 1), (_E5, 1/2, True), (_E4, 3/2), (_E5, 1/2, True), (_A4, 1/4), (_Ad4, 1/4),
    (_B4, 1), (_B5, 1/2, True), (_B4, 1, True), (_B4, 1/4, True), (_B4, 1/4, True), (_Fd5, 1/4), (_E5, 1/4, True), (_D5, 1/4, True), (_B4, 1/4, True),
    (_G4, 1), (_G5, 1/2, True), (_G4, 3/2), (_G5, 1/2, True), (_C5, 1/4), (_Cd5, 1/4),
    (_D5, 1), (_D6, 1/2, True), (_A4, 3/2), (_A5, 1/2, True), (0, 1/2, True)
    ]
    
def startStop(buzzer):
    if buzzer.playMusic.is_set():
        buzzer.playMusic.clear()
    else:
        buzzer.playMusic.set()
        

class Buzzer:
    
    # In microsecondi, come intero
    lowNotePeriod = 1000000//LOW_NOTE_FREQUENCY
    highNotePeriod =  1000000//HIGH_NOTE_FREQUENCY
    
    def __init__(self, buzzerPin, modeHandler):
        self.buzzerPin = buzzerPin
        self.modeHandler = modeHandler
        self.length = 60000//TEMPO
        self.playMusic = threading.Event()
        self.musicThread = thread(self.playSong, prio=PRIO_LOWEST)
        self.lock = threading.Lock()
        
    
    # Suono all'accensione del led
    def playTurnOn(self):
        self.playMusic.clear()
        self.lock.acquire()
        
        # Imposto il periodo del buzzer ed il duty cycle a 50%
        if not self.modeHandler.muted:
            p = self.lowNotePeriod
            pwm.write(self.buzzerPin, p, p//2, MICROS)
            sleep(200) 
            p = self.highNotePeriod
            pwm.write(self.buzzerPin, p, p//2, MICROS)
            sleep(300)
        
        pwm.write(self.buzzerPin, 0, 0, MICROS)
        self.lock.release()
        
    
    # Suono allo spegnimento del led
    def playTurnOff(self):
        self.playMusic.clear()
        self.lock.acquire()
        
        if not self.modeHandler.muted:
            p = self.highNotePeriod
            pwm.write(self.buzzerPin, p, p//2, MICROS)
            sleep(200) 
            p = self.lowNotePeriod
            pwm.write(self.buzzerPin, p, p//2, MICROS)
            sleep(300)
        
        pwm.write(self.buzzerPin, 0, 0, MICROS)
        self.lock.release()
        
        
    def playSong(self):
        while(True):
            self.playMusic.wait()
            self.lock.acquire()
            i = 0
            while self.playMusic.is_set() and i < len(musicSheets):
                note, size, dotted = musicSheets[i]
                if dotted != True:
                    pwm.write(self.buzzerPin, note, note//2, MICROS)
                    sleep(int(size*self.length))
                else:
                    pwm.write(self.buzzerPin, note, note//2, MICROS)
                    sleep(int(1/2*size*self.length))
                    pwm.write(self.buzzerPin, 0, 0, MICROS)
                    sleep(int(1/2*size*self.length))
                i += 1
                i %= len(musicSheets)
            pwm.write(self.buzzerPin, 0, 0, MICROS)
            self.lock.release()
            
