# import gspread
# from db import database
# import asyncio
# from datetime import datetime

class sheets:
    def __init__(self):
        """Initialises the connection to the google sheet using the google sheets API
        """
        self.gc1 = gspread.service_account(filename='credantials.json')
        self.sh1 = self.gc1.open_by_key('1b53CQsonQUc2DCce_fnXoeHTh2qXH1l8wuWrzDHqB4k')
        self.courseWorksheet = self.sh1.sheet1
        self.res1 = self.courseWorksheet.get_all_records()

        # self.gc2 = gspread.service_account(filename='credantials.json')
        self.sh2 = self.gc1.open_by_key('1J3cPjzjKt7C20qA6SKbMP4uiy95oTLgCJEqW0fD4BLI')
        self.courseShedule = self.sh2.sheet1
        self.scheduleResults = self.courseShedule.get_all_records()
        pass

    # def getCourseData(self):
    #     res = self.courseWorksheet.get_all_records()
    #     print(res)
    
    def checkCourseExistance(self,course,dbObj):
        """Checks if the course provided by the parameter above exists in the database

        :param course: Code of course to be checked
        :type course: String
        :param dbObj: Database object from db class with functions for accessing remote database
        :type dbObj: db
        :return: returns true of the course exists in the db and false if the course does not exist in the database
        :rtype: bool
        """
        query = "SELECT * FROM course WHERE  code = '{}'".format(course)
        cursor = dbObj.getDB()
        cursor.execute(query)

        check = False
        for item in cursor:
            # check = True
            return True
            # break
        return False
    
    async def AddCourse(self,dbObj):
        """Adds the course specified to the database

        :param dbObj: Database object from db class with functions for accessing remote database
        :type dbObj: db
        """
        query = ""
        first_entry = True
        moreValues = None # Stores value for insert statement with multiple row entries
        # Checking if items are in database and if not adding them to query
        for entry in self.res1:
            course_code = entry['Course Code']
        
            # If entry already exists in database
            if( not self.checkCourseExistance(course_code,dbObj)):

                if(first_entry):
                    course_name = entry['Course name']
                    query = "INSERT INTO course(code,course_name) VALUES('{}','{}');".format(course_code,course_name)
                    first_entry = False
                else:
                    moreValues = "('{}','{}');".format(course_code,course_name)
                
                query = self.gatherInsertQueries(query,moreValues)
        
        print(query)
        await dbObj.insertData(query)
    
    async def showCourses(self,dbObj):
        """Prints all the courses that are available in the database

        :param dbObj: Database object from db class with functions for accessing remote database
        :type dbObj: db
        """
        cursor = dbObj.getDB()
        cursor.execute("SELECT * FROM course ORDER BY code ASC;")

        for item in cursor:
            out = "Course code: {}, Course name: {}".format(item[0],item[1])
            print(out)
       
    
    def gatherInsertQueries(self,query,newValues=None):
        """Combine multiple insert queries into one query,
        In order to allow one call to the db instead of multiple calls

        :param query: The first values to be inserted in the table, (Leading statements of the insert statements)
        :type query: String
        :param newValues: The additional values that have to the leading statement of the query, defaults to None
        :type newValues: String, optional
        :return: The new query that has old values and the new values
        :rtype: String
        """
        if(newValues is not None):
            query = query[:-1] + ", "+ newValues
        else:
            query = query
        return query


    async def updateLabSchedule(self,dbObj):
        """Updates the lab scheduled in the database based on entries on the google sheets document

        :param dbObj: Database object from db class with functions for accessing remote database
        :type dbObj: db
        """
        # Initialise values to be used in loop
        moreValues = None # Stores value for insert statement with multiple row entries
        schedule_list = [] # List to be used to create register ID
        invalid_data = False
        query = ""
        first_entry = True

        for entry in self.scheduleResults:

            date = entry['date (yyyy/mm/dd)'] 
            start = entry['start time(hh:mm:ss)']
            end = entry['end time(hh:mm:ss)']
            course_code = entry['course code']
            activity = entry['activity'] 

            startDateTime = datetime.strptime(date+" "+start, "%m/%d/%Y %H:%M:%S")
            endDateTime = datetime.strptime(date+" "+end, "%m/%d/%Y %H:%M:%S")

            schedule_id = self.createScheduleID(course_code,startDateTime,start)
            print(schedule_id)
            
            if( not self.checkLabScheduleExistance(schedule_id,dbObj)):
                if( not self.checkLabScheduleExistance(schedule_id,dbObj)):
                    
                    if(first_entry):
                        query = "INSERT INTO lab_schedule(schedule_id,start,end,code,activity) VALUES('{}','{}','{}','{}','{}');".format(schedule_id,startDateTime,endDateTime,course_code,activity)
                        first_entry = False
                    else:
                        moreValues = "('{}','{}','{}','{}','{}');".format(schedule_id,startDateTime,endDateTime,course_code,activity)
                    query = self.gatherInsertQueries(query,moreValues)
                    schedule_list.append((schedule_id,course_code))
        
        print(query)
        await dbObj.insertData(query)
        # cursor.execute(query)
        await self.generateRegister(schedule_list,dbObj)


    async def showRegister(self,schedule_id,dbObj):
        """prints out the register information for a specific course schedule

        :param schedule_id: The schedule id of the register that must be printed out
        :type schedule_id: String
        :param dbObj: Database object from db class with functions for accessing remote database
        :type dbObj: db
        """
        cursor = dbObj.getDB()
        query = "SELECT * FROM register WHERE schedule_id = '{}' ORDER BY student_no ASC;".format(schedule_id)
        cursor.execute(query)

        for item in cursor:
            out = "Student_no: {}, Status: {}".format(item[2],item[1])
            print(out)
    
    async def showLabSchedule(self,course,dbObj):
        """Shows the lab schedules that are scheduled in the database for a specific course

        :param course: The course code in which schedules need to be displayed
        :type course: String
        :param dbObj: Database object from db class with functions for accessing remote database
        :type dbObj: db
        """
        cursor = dbObj.getDB()
        query = "SELECT * FROM lab_schedule WHERE code = '{}' ORDER BY start ASC;".format(course)
        cursor.execute(query)

        for item in cursor:
            out = "schedule_id: {}, start: {}, end: {}, code: {}, activity: {}".format(item[0],item[1],item[2],item[3],item[4])
            print(out)

    def createScheduleID(self,code,start,time):
        """Generates a schedule ID give the course code, start time and end time of the schedule

        :param code: Course code in which the schedule is being generated for
        :type code: String
        :param start: Start date of the scheduled activity
        :type start: DateTime
        :param time: Start time for the scheduled activity
        :type time: DateTime
        :return: Returns the schedule ID of the activity
        :rtype: String
        """
        date_portion = str(start)[:10]
        time_portion = str(time)[:2]
        code_portion = str(code)[3:]
        schedule_id = code_portion+"-"+date_portion+"-"+time_portion
        return schedule_id
    
    def checkLabScheduleExistance(self,schedule_id,dbObj):
        """Checks if the a specific schedule already exists in the database, returns True if exists and false if does not exist.

        :param schedule_id: The schedule id that is being checked in the database
        :type schedule_id: String
        :param dbObj: Database object from db class with functions for accessing remote database
        :type dbObj: db
        :return: Returns true if activity with schedule_id exists in database, and False if it does not exist
        :rtype: bool
        """
        query = "SELECT * FROM lab_schedule WHERE schedule_id = '{}'".format(schedule_id)
        cursor = dbObj.getDB()
        cursor.execute(query)

        check = False
        for item in cursor:
            return True
        return False 

    def generateRegisterId(self,student_no,schedule_id):
        """Generates register ID given a student number and schedule ID for an activity

        :param student_no: Student number of student whose is being added to the register
        :type student_no: String
        :param schedule_id: The scheduled activity in which the register ID is being generated for
        :type schedule_id: String
        :return: Returns the generated register ID
        :rtype: String
        """
        return student_no+"_"+schedule_id

    async def generateRegister(self,schedule_list,dbObj):
        """Generate the register of an activity that is scheduled and added to the database 

        :param schedule_list: The list of scheduled activities that needs registers to be generated
        :type schedule_list: list
        :param dbObj: Database object from db class with functions for accessing remote database
        :type dbObj: db
        """
        
        for schedule in schedule_list:
            course_code = schedule[1]
            schedule_id = schedule[0] 

            # Get all students
            cursor = dbObj.getDB()
            query = "SELECT * FROM enrolls WHERE code = '{}';".format(course_code)
            cursor.execute(query)

            # Initialise values to be used in loop
            first = True
            moreValues = None

            for entry in cursor:
                student_no = entry[1]
                status = 0
                registerId = self.generateRegisterId(student_no,schedule_id)

                if (first):
                    query = "INSERT INTO register(register_id,status,student_no,schedule_id) VALUES('{}','{}','{}','{}');".format(registerId,status,student_no,schedule_id)
                    first = False
                else:
                    moreValues = "('{}','{}','{}','{}');".format(registerId,status,student_no,schedule_id)

                query = self.gatherInsertQueries(query,moreValues)
            
            await dbObj.insertData(query)
    
    async def createEnrollsID(self,student_id,code):
        """Creates the enrolls ID that is required when a student is enrolled in a course

        :param student_id: Student number of the student being enrolled
        :type student_id: String
        :param code: The course code of the that student is enrolling in
        :type code: String
        :return: The enrolls ID of the student
        :rtype: String
        """
        return code[3:]+"_"+student_id

    
    
    # async postTostudent

# Initialisations
# dbObj = database("eee4022sdatabase-do-user-9871310-0.b.db.ondigitalocean.com",
#     "admin",
#     "aGAPX1Hn5TdTE-4I",
#     "lab_system",
#     "25060",
#     "mysql_native_password"
#     )
# sheetObj = sheets()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(sheetObj.updateLabSchedule(dbObj))
# loop.run_until_complete(sheetObj.AddCourse(dbObj))
# loop.run_until_complete(sheetObj.showCourses(dbObj))
# sheetObj.getCourseData()