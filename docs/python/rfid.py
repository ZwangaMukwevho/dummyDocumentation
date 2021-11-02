#!/usr/bin/env python

# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522
# from LED import LED

# reader = SimpleMFRC522()

class rfid:
        # reader = SimpleMFRC522()
        # LEDObj = LED()
        def __init__(self):
               
                # GPIO.setmode(GPIO.BCM)
                pass
        
        def writeData(self):
                """ Wrties data to RFID card
                """
                try:
                        text = input('New data:')
                        print("Now place your tag to write")
                        # reader.write(text)
                        print("Written")
                finally:
                        pass
                        # GPIO.cleanup()
        
        async def readData(self):
                """Reads Data from the rfid card
                Turns on green LED if access granted
                Turns on RED LED if access denied"""
                try:
                        # print("running")
                        # id, text = reader.read()
                        # print(text)
                        
                        text = text.strip()
                        return text
                finally:
                        # GPIO.cleanup()
                        return text