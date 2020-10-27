import logging
import blynklib
import generate_json
from gpiozero import LED
from sensor import Sensor


# Auth and Initialize Blynk
#blynk = blynklib.Blynk('i1mAIy3lgcyABxYWH_8T3grDgvjN3mkT', server='192.168.0.17', port='8080') # Blynk email feature wasnt working in the Local Server
blynk = blynklib.Blynk("9dmN1S97LWeMHF05iFO8Frydk_vG1s-R")

# Initialize Log File
logging.basicConfig(filename='moisture_read.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Variable Section
red_led = LED(17)
green_led = LED(27)
blue_led = LED(22)

LIMIT_FLAG = 2  # 1 High / 2 Normal / 3 Low (Dry - Error)
green_led.on()

# Instanciate Sensor class
sensorData = Sensor()

@blynk.handle_event('read V5')
def read_virtual_pin_handler(pin):
    """ Function to Manage the Value Display App Widget """
    try:
        # send moisture read value to Virtual Pin
        blynk.virtual_write(5, track_moisture_level())

        if LIMIT_FLAG == 3:
            blynk.set_property(5, 'color', '#FF0000') # Red
            blynk.set_property(6, 'color', '#FF0000')
            blynk.virtual_write(6, "LOW")
        elif LIMIT_FLAG == 2:
            blynk.set_property(5, 'color', '#FFD700') # Yellow
            blynk.set_property(6, 'color', '#FFD700')
            blynk.virtual_write(6, "NORMAL")
        else:
            blynk.set_property(5, 'color', '#00BFFF') # Blue
            blynk.set_property(6, 'color', '#00BFFF')
            blynk.virtual_write(6, "HIGH")
    except Exception as e:
        logging_write(e)

def track_moisture_level():
    """ Function to Track Moisture Level - Returns Moisture Value """
    try:
        normal_level_init = 470
        low_level_init = 560

        global LIMIT_FLAG
        sensor_read = sensorData.read_moisture()
        generate_json.define_structure("moisture", sensor_read)

        if sensor_read > low_level_init:
            if LIMIT_FLAG != 3:
                # When it is dry (Moisture Level Low)
                LIMIT_FLAG = 3
                blynk.notify('Moisture Level Low! Irrigation Needed')
                blynk.email('brunocpp@gmail.com', 'Alert: Moisture Level Low',
                            'Moisture Level Low! Irrigation Needed')
                logging_write()
        elif normal_level_init <= sensor_read <= low_level_init:
            if LIMIT_FLAG != 2:
                LIMIT_FLAG = 2
                logging_write()
        else:
            if LIMIT_FLAG != 1:
                LIMIT_FLAG = 1
                logging_write()
        return sensor_read

    except Exception as e:
        logging_write(e)

def logging_write(e=None):
    """ Logging Function - Write to log """
    try:
        if e is not None: # Exception errors
            logging.error(e)

        if LIMIT_FLAG == 3:
            print('Moisture Level: Low (Dry)')
            logging.info('| Moisture Level Low (Dry)')
            red_led.on()
            green_led.off()
            blue_led.off()
        elif LIMIT_FLAG == 2:
            print('Moisture Level: Normal')
            logging.info('| Moisture Level: Normal')
            red_led.off()
            green_led.on()
            blue_led.off()
        else:
            print('Moisture Level: High')
            logging.warning('| Moisture Level: High')
            red_led.off()
            green_led.off()
            blue_led.on()
    except Exception as e:
        logging_write(e)

while True:
    try:
        blynk.run()
    except Exception as e:
        logging_write(e)
