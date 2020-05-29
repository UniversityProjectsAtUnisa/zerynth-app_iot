import i2c
import config as cfg
import math

class LightSensor(i2c.I2C):
    DEVICE     = 0x23 # Default device I2C address
    POWER_DOWN = 0x00 # No active state
    POWER_ON   = 0x01 # Power on
    RESET      = 0x07 # Reset data register value
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_1 = 0x20
    # Start measurement at 0.5lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_2 = 0x21
    # Start measurement at 4lx resolution. Time is typically 16ms. 
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_LOW_RES_MODE = 0x23
    
    MAX_LUX_DETECTED = cfg.MAX_LUX_DETECTED
    
    
    def __init__(self, drvname, sensitivity=69):
        i2c.I2C.__init__(self, drvname, self.DEVICE)
        self.start()
        print('Initialized')
        self.set_sensitivity(sensitivity)

    def _set_mode(self, mode):
        self.mode = mode
        self.write([self.mode])

    def power_down(self):
        self._set_mode(self.POWER_DOWN)

    def power_on(self, reset=True):
        self._set_mode(self.POWER_ON)
        if reset:
            self._set_mode(self.RESET)

    def oneshot_low_res(self):
        self._set_mode(self.ONE_TIME_LOW_RES_MODE)

    def oneshot_high_res(self):
        self._set_mode(self.ONE_TIME_HIGH_RES_MODE_1)

    def oneshot_high_res2(self):
        self._set_mode(self.ONE_TIME_HIGH_RES_MODE_2)

    def set_sensitivity(self, sensitivity=69):
        """ Set the sensor sensitivity.
            Valid values are 31 (lowest) to 254 (highest), default is 69.
        """
        if sensitivity < 31:
            self.mtreg = 31
        elif sensitivity > 254:
            self.mtreg = 254
        else:
            self.mtreg = sensitivity
        self.power_on()
        self._set_mode(0x40 | (self.mtreg >> 5))
        self._set_mode(0x60 | (self.mtreg & 0x1f))
        self.power_down()

    def get_result(self):
        """ Return current measurement result in lx. """   
        data = self.write_read(self.mode, 2)
        count = data[0] | (data[1]&0xff)<<8
        mode2coeff =  2 if (self.mode & 0x03) == 0x01 else 1
        ratio = 1/(1.2 * (self.mtreg/69.0) * mode2coeff)
        return ratio*count

    def wait_for_result(self, additional=0):
        basetime = 18 if (self.mode & 0x03) == 0x03 else 128
        sleep(basetime * int(self.mtreg/69.0) + additional)


    def do_measurement(self, mode, additional_delay=0):
        """ 
        Perform complete measurement using command
        specified by parameter mode with additional
        delay specified in parameter additional_delay.
        Return output value in Lx.
        """
        self.power_on()
        self._set_mode(mode)
        self.wait_for_result(additional=additional_delay)
        return self.get_result()
        
    def toPercentage(self, brightness):
        if brightness == 0:
            return 0
        else:
            return 100 * (math.log(brightness) / math.log(self.MAX_LUX_DETECTED))

    def measure_low_res(self, percentage=True, additional_delay=0):
        brightness = self.do_measurement(self.ONE_TIME_LOW_RES_MODE, additional_delay)
        if brightness > self.MAX_LUX_DETECTED:
            brightness = self.MAX_LUX_DETECTED
        brightness = self.toPercentage(brightness) if percentage else brightness
        return math.ceil(brightness)

    def measure_high_res(self, percentage=True, additional_delay=0):
        brightness = self.do_measurement(self.ONE_TIME_HIGH_RES_MODE_1, additional_delay)
        if brightness > self.MAX_LUX_DETECTED:
            brightness = self.MAX_LUX_DETECTED
        brightness = self.toPercentage(brightness) if percentage else brightness
        return math.ceil(brightness)

    def measure_high_res2(self, percentage=True, additional_delay=0):
        brightness = self.do_measurement(self.ONE_TIME_HIGH_RES_MODE_2, additional_delay)
        if brightness > self.MAX_LUX_DETECTED:
            brightness = self.MAX_LUX_DETECTED
        brightness = self.toPercentage(brightness) if percentage else brightness
        return math.ceil(brightness)