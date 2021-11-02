# from rfid import rfid
# import RPi.GPIO as GPIO
# from temp import temp
# from rfid import rfid
# from LED import LED
# from db import database
import time
import asyncio

async def checkTemp(tempObj,LEDObj,loop):
    """Samples temperature reading and returns it, and also flashes RED or GREEN LED based on weather the temp reading is higher than threshold.

    :param tempObj: Object from Temp class
    :type tempObj: temp
    :param LEDObj: Object from LED class
    :type LEDObj: LED
    :param loop: Main event loop to be used to run coroutines concurrenlty
    :type loop: asyncio application
    :return: Temperature value of target object
    :rtype: float
    """
    tic = time.perf_counter()
    tempValue = await asyncio.gather(tempObj.readTemp())
    toc = time.perf_counter()  
    print(f"Time taken to get Temp readings: {toc - tic:0.4f} seconds")
    if tempValue[0] < 35.00 and tempValue[0] > 29.00:
        tic = time.perf_counter() 
        asyncio.gather(LEDObj.swichOnTempGreen())
        toc = time.perf_counter()  
        print(f"Time taken to toggle red LED: {toc - tic:0.4f} seconds")  
        return tempValue
        
    else:
        tic = time.perf_counter()
        asyncio.gather(LEDObj.swichOnTempRed())
        toc = time.perf_counter()  
        print(f"Time taken to toggle green LED :{toc - tic:0.4f} seconds")  
        return tempValue
        
async def checkRficCard(text,LEDObj,dbObj,loop):
    """Checks if student number exists in database and returns True if it exists in database, and False otherwise. Green LED toggled in True case, Red toggled in False case

    :param text: The student number
    :type text: String
    :param LEDObj: Object of LED class
    :type LEDObj: LED
    :param dbObj: Database object from db class with functions for accessing remote database
    :type dbObj: db
    :param loop: Main event loop to be used to run coroutines concurrenlty]
    :type loop: asyncio application
    :return: True if student number exists in database, and false otherwise
    :rtype: boolean
    """
    tic = time.perf_counter()
    results = await dbObj.findStudentNumber(text)
    toc = time.perf_counter()
    print(f"Time taken to check validate student in DB: {toc - tic:0.4f} seconds")
    
    if len(results) != 0:
        tic = time.perf_counter()
        asyncio.gather(LEDObj.swichRfidOnRed())  
        toc = time.perf_counter()  
        print(f"Time taken to toggle red LED: {toc - tic:0.4f} seconds")    
        return True
    else:
        tic = time.perf_counter()
        asyncio.gather(LEDObj.swichRfidOnGreen())
        toc = time.perf_counter()  
        print(f"Time taken to toggle green LED: {toc - tic:0.4f} seconds")     
        return False
    pass


if __name__ == "__main__":

    tic = time.perf_counter()
    tempObj = temp()  # Temp class object
    rfidObj = rfid() # rfid object object
    LEDObj = LED() # #LED class object
    dbObj = database("eee4022sdatabase-do-user-9871310-0.b.db.ondigitalocean.com",
    "admin",
    "aGAPX1Hn5TdTE-4I",
    "lab_system",
    "25060",
    "mysql_native_password") # database class object
    toc = time.perf_counter()
    print(f"Time taken to connect to the database is: {toc - tic:0.4f} seconds")
    # rfidObj.readData()


    # print(GPIO.getmode())
    # mfrc22 module uses BCM mode, if you set-up GPIO using board mode, the data won't be read
    # while(True):
        
    # print("provide card")
    # student_no = "SHVNKA005"
    # print("1")
    # rfidCheck = checkRficCard(student_no,LEDObj,dbObj)
    # # tempCheck = checkTemp(tempObj,LEDObj)
    # print("2")
    # # dbObj.postTempReading(student_no,tempCheck)
    # while(True):
    
    # loop = asyncio.get_event_loop()
    # tempCheck = loop.run_until_complete(checkTemp(tempObj,LEDObj,loop))
    # loop.run_until_complete(dbObj.postTempReading(student_no,tempCheck[0]))
    # print("")

    loop = asyncio.get_event_loop()
    count = 0
    for i in range(1):
        print("count "+str(count))
        count += 1
        
        tic = time.perf_counter()
        student_no = loop.run_until_complete(rfidObj.readData())
        # student_no = "ABCDEF001"
        toc = time.perf_counter()
        print(f"Time taken to read data from RFID card: {toc - tic:0.4f} seconds")

        rfidCheck = loop.run_until_complete(checkRficCard(student_no,LEDObj,dbObj,loop))
        
        if(rfidCheck):
            tempCheck = loop.run_until_complete(checkTemp(tempObj,LEDObj,loop))

            if(tempCheck[0] <35.00 ):

                pass
                tic = time.perf_counter()
                dbObj.markAttendance(student_no)
                toc = time.perf_counter()
                print(f"Time taken to mark attendance register: {toc - tic:0.4f} seconds")

                tic = time.perf_counter()
                dbObj.postTempReading(student_no,tempCheck)
                toc = time.perf_counter()
                print(f"Time taken to post data to temp log: {toc - tic:0.4f} seconds")

                tic = time.perf_counter()
                # Run marking of attendance register and posting to database concurrently
                loop.run_until_complete(asyncio.gather(dbObj.markAttendance(student_no),dbObj.postTempReading(student_no,tempCheck[0])))
                toc = time.perf_counter()
                print(f"Time taken to mark attendance register: {toc - tic:0.4f} seconds")
                print("")

