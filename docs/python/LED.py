import RPi.GPIO as GPIO
import time
import asyncio

class LED:
    
    def __init__(self): 
            # GPIO.setmode(GPIO.BOARD)
            pass
    
    async def swichRfidOnGreen(self):
        """Switches on green Green LED on and off for the RFID subsystem
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
     
        GPIO.setup(24,GPIO.OUT)
        GPIO.output(24,GPIO.HIGH)

        # GPIO.setup(18,GPIO.OUT)
        # GPIO.output(18,GPIO.HIGH)
        # time.sleep(1)
        time.sleep(0.7)
        # await asyncio.sleep(0.7)

        # GPIO.output(18,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
    
    async def swichRfidOnRed(self):
        """Switches on green RED LED on and off for the RFID subsystem
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
     
        # GPIO.setup(16,GPIO.OUT)
        # GPIO.output(16,GPIO.HIGH)
        GPIO.setup(23,GPIO.OUT)
        GPIO.output(23,GPIO.HIGH)

        # time.sleep(1)
        time.sleep(0.7)
        # await asyncio.sleep(0.7)
        # GPIO.output(16,GPIO.LOW)  
        GPIO.output(23,GPIO.LOW) 

    async def swichOnTempRed(self):
        """Switches on green RED LED on and off for the Temperature subsystem
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
     
        # GPIO.setup(11,GPIO.OUT)
        # GPIO.output(11,GPIO.HIGH)
        # time.sleep(1)

        # GPIO.output(11,GPIO.LOW)

        GPIO.setup(17,GPIO.OUT)
        GPIO.output(17,GPIO.HIGH)
        # time.sleep(1)
        time.sleep(0.7)
        # await asyncio.sleep(0.7)

        GPIO.output(17,GPIO.LOW)

    async def swichOnTempGreen(self):
        """Switches on green GREEEN LED on and off for the TEMP subsystem
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
     
        # GPIO.setup(13,GPIO.OUT)
        # GPIO.output(13,GPIO.HIGH)
        # time.sleep(1)

        # GPIO.output(13,GPIO.LOW)
        GPIO.setup(27,GPIO.OUT)
        GPIO.output(27,GPIO.HIGH)
        # time.sleep(1)
        time.sleep(0.7)
        # await asyncio.sleep(0.7)

        GPIO.output(27,GPIO.LOW)
    
# LEDObj = LED()
# LEDObj.swichRfidOnGreen()
# LEDObj.swichRfidOnRed()
# LEDObj.swichOnTempRed()
# LEDObj.swichOnTempGreen()
# GPIO.cleanup()      
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(23,GPIO.OUT)
# GPIO.setup(24,GPIO.OUT)
# print("LED on")
# GPIO.output(23,GPIO.HIGH)
# GPIO.output(24,GPIO.HIGH)
# time.sleep(1)
# print("LED off")
# GPIO.output(23,GPIO.LOW)
# GPIO.output(24,GPIO.LOW)
