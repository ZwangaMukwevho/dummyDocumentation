#from sheets import sheets
#import asyncio
#from db import database
#from datetime import datetime

class admin:
    def __init__(self,dbObj,sheetsObj):
        """Constructor that initilizes the objects (db, sheets) to be used within the class

        :param dbObj: [Database object from db class with funtions for accessing remote database]
        :type dbObj: [db]
        :param sheetsObj: [sheets object that access the google sheets that is used for scheduling lab activities]
        :type sheetsObj: [sheets]
        """
        self.sheetsObj = sheetsObj
        self.dbObj = dbObj
        self.loop = asyncio.get_event_loop()
    
    def welcomeDisplay(self):
        """Displays the hello messaage when the CLI interface is launched
        """
        os.system('clear')
        print('              __________                               _________')
        print('|         |  |             |           |              /          \ ')
        print('|         |  |             |           |             /            \ ')
        print('|         |  |             |           |            |              |')
        print('|---------|  |----------   |           |            |              |')
        print('|         |  |             |           |            |              |')
        print('|         |  |             |           |             \            /')
        print('|         |  |__________   |__________ |__________    \_________ /')
    
    def dispayMenue(self):
        """Main loop that prompts user for input and prints result on screen
        """
        keepRunning = True
        while(keepRunning):

            # print("")
            print("Press '1' to update courses in database:")
            print("press '2' to update lab schedule:")
            print("Press '3' to view courses in databases:")
            print("Press '4' to view register for a specific course:")
            print("Press '5' to view lab_schedules for a specific course:")
            print("Press '6' to change a students attendance status on register: ")
            print("print 'q' to quit: ")
            inValue = input("")

            if inValue == '1':
                print("updating courses")
                self.loop.run_until_complete(self.sheetsObj.AddCourse(self.dbObj))
                print("done updating courses")
            
            if inValue == '2':
                print("updating lab_schedule")
                self.loop.run_until_complete(self.sheetsObj.updateLabSchedule(self.dbObj))
                print("done updating lab_schedule")
                print("Corresponding registers for the lab schedule have been created")
            
            if inValue == '3':
                print("")
                print("The following courses are on the database")
                self.loop.run_until_complete(self.sheetsObj.showCourses(self.dbObj))
            
            if inValue == '4':
                inValue = input("Enter the schedule_id: ")
                print(f"The register for {inValue} is: ")
                self.loop.run_until_complete(self.sheetsObj.showRegister(inValue,self.dbObj))
                print("")

            if inValue == '5':
                inValue = input("Enter the course code: ")
                print(f"The current available schedule activities  for {inValue} are: ")
                self.loop.run_until_complete(self.sheetsObj.showLabSchedule(inValue,self.dbObj))
                print("")

            if inValue == '6':
                inValue = input("Enter the schedule ID of activity: ")
                print(f"The current register for schedule ID {inValue} is:")
                print("")
                self.loop.run_until_complete(self.sheetsObj.showRegister(inValue,self.dbObj))
                print("")
                student_no = input("Enter the student number of student number of student: ")
                print("")
                status = eval(input("Enter '1' to mark student as present and '2' to mark student as absent for activity: "))                
                print("")
                self.loop.run_until_complete(self.dbObj.updateStudentRegister(student_no,inValue,status))
            
            if inValue == 'q':
                print("quitting")
                keepRunning = False

    
    # def updateCourse(self):
    #     pass


if __name__ == "__main__":
    dbObj = database("eee4022sdatabase-do-user-9871310-0.b.db.ondigitalocean.com",
    "admin",
    "aGAPX1Hn5TdTE-4I",
    "lab_system",
    "25060",
    "mysql_native_password"
    )
    # datetime_obj = datetime.strptime("10/15/2021", "%m/%d/%Y")
    # print(datetime_obj)
    sheetObj = sheets()
    adObj = admin(dbObj,sheetObj)
    adObj.welcomeDisplay()
    adObj.dispayMenue()



