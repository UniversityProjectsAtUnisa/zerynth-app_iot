from lwmqtt import mqtt

SSID = "Della Rocca"
PASSWORD = "xDrxQjn7b7"

def connect():
    from espressif.esp32net import esp32wifi as wifi_driver
    wifi_driver.auto_init()
    
    
    print("Establishing Link...")
    try:
        from wireless import wifi
        wifi.link(SSID, wifi.WIFI_WPA2, PASSWORD)
    except Exception as e:
        print("ooops, something wrong while linking :(", e)
        while True:
            sleep(1000)
    
            
class Client(mqtt.Client):
    def breconnect(self):
        print("Tentativo di riconnessione in corso...")

    def aconnect(self):
        self.publish("current/connected", "True", qos=1, retain=True)
        
    def __init__(self, client_id, clean_session=True):
        mqtt.Client.__init__(self, client_id, clean_session)
        self.set_will("current/connected", "False", qos=1, retain=True)
        
        for retry in range(10):
            try:
                self.connect("test.mosquitto.org", 10, breconnect_cb=self.breconnect, aconnect_cb=self.aconnect)
                break
            except Exception as e:
                print("connecting...")
        print("connected.")