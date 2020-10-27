import logging
import time
from grove.adc import ADC

logging.basicConfig(filename='moisture_read.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Sensor:
    """ Class that manages Sensor data """
    def __init__(self):
        self.aio = ADC()

    def read_moisture(self):
        """ Method that returns Moisture Sensor reading """
        try:
            moisture_read = self.aio.read(0)
            time.sleep(3) # Wait 3 seconds
            return moisture_read
        except Exception as error:
            logging.error(error)
