import streams
import i2c


class SoundSensor:
    ADDR_ADC121 = 0x50
    
    def __init__(self, drvname):
        self.port = i2c.I2C(drvname, self.ADDR_ADC121)
        self.port.start()


# DAL DATASHEET!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from Adafruit_I2C import Adafruit_I2C
import time

ADDR_ADC121 = 0x50

REG_ADDR_RESULT = 0x00
REG_ADDR_ALERT = 0x01
REG_ADDR_CONFIG = 0x02
REG_ADDR_LIMITL = 0x03
REG_ADDR_LIMITH = 0x04
REG_ADDR_HYST = 0x05
REG_ADDR_CONVL = 0x06
REG_ADDR_CONVH = 0x07

i2c = Adafruit_I2C(ADDR_ADC121)

class I2cAdc:
    def __init__(self):
        i2c.write8(REG_ADDR_CONFIG, 0x20)
        
    def read_adc(self):
        "Read ADC data 0-4095."
        data_list = i2c.readList(REG_ADDR_RESULT, 2)
        #print 'data list', data_list
        data = ((data_list[0] & 0x0f) << 8 | data_list[1]) & 0xfff
        return data



# DAL DRIVER DEL PROFESSORE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# # HTU21D sensor driver
# Created at 2019-04-29 17:19:06.368110

import streams
import i2c


streams.serial()

def my_init():
    global port
    port=i2c.I2C(I2C0, 0x40)
    port.start()
    print('initialised')

def init_HTU21D(my_p):
    # sensor software reset 
    my_p.write([0xFE])  
    sleep(500)
    #send the command for enabling the sampling mode for humidity and temperature (0 -> 12bit for RH and 14 bits for T)
    my_p.write([0xE6])
    my_p.write([0x00])
    
    
    

def build_value(hi,lo):
    return (hi << 8 | (lo & 0xFC))


    
try:
    global port
    my_init()
    init_HTU21D (port)

    while True:
        #read humidity 
        port.write(0xE5)
        sleep(20)
        data=port.read(2)
        humid_raw_value = build_value(data[0], data[1])
        print('humidity raw value = ', humid_raw_value)
        humid_value = ((125*humid_raw_value)/(65536))-6
        print('humidity  value = ', humid_value)
        print('status bits for humidity', data[1] & 0x03)
        print('_____________________________________')
        #read temp value
        port.write(0xE3)
        sleep(60)
        data=port.read(2)
        temp_raw_value = build_value(data[0], data[1])
        print('temperature raw value = ', temp_raw_value)
        temp_value = ((175.72*temp_raw_value)/(65536))-46.85
        print('temperature value = ', temp_value)
        print('status bits for temp', data[1] & 0x03)
        print('_____________________________________')
        sleep(2000)
except Exception as e:
    print(e)
    