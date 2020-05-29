from mqtt import mqtt

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
            
def breconnect():
    print("Tentativo di riconnessione in corso...")
            
class Client(mqtt.Client):
    def __init__(self, client_id, clean_session=True):
        mqtt.Client.__init__(self, client_id, clean_session)
        
        for retry in range(10):
            try:
                self.connect("test.mosquitto.org", 60, breconnect_cb=breconnect)
                break
            except Exception as e:
                print("connecting...")
        print("connected.")