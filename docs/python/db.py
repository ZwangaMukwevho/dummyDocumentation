# import MySQLdb
# import mysql.connector
# import asyncio
# from datetime import datetime

class database:
    db = None
    cursor = None

    def __init__(self,hostVar,userVar,passwdVar,databaseVar,portVar,auth_pluginVar):
        """Constructor that connects to the database remotely

        :param hostVar: host IP address or Host name
        :type hostVar: String
        :param userVar: Name of user connecting to database
        :type userVar: String
        :param passwdVar: Passwrod for the database
        :type passwdVar: String
        :param databaseVar: Name of database being connected to on the mysql server
        :type databaseVar: String
        :param portVar: Port number for connecting to database
        :type portVar: String
        :param auth_pluginVar: Type of plugin to be used for Authenitcatiting the database
        :type auth_pluginVar: String
        """
        self.db = mysql.connector.connect(
        host= hostVar,
        user=userVar,
        passwd=passwdVar,
        database=databaseVar,
        port =portVar,
        auth_plugin=auth_pluginVar)

        self.cursor = self.db.cursor()
    
    async def findStudentNumber(self,studentNumber):
        """Returns results Select statement that looks for a student number in the student table

        :param studentNumber: MKWZWA0003
        :type studentNumber: String
        :return: List of records obtained from the query
        :rtype: List
        """
        query = "SELECT * FROM student WHERE student_no = '{}';".format(studentNumber)
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def markRegister(self,studentNumber,activity): 
        """[summary]

        :param studentNumber: [description]
        :type studentNumber: [type]
        :param activity: [description]
        :type activity: [type]
        """
        return ""
    
    def getDB(self):
        return self.cursor
    
    async def insertData(self,query):
        """Inserts data to the enrolls the database using the given qeury

        :param query: query to be executed on the database
        :type query: String
        """
        self.cursor.execute(query)
        self.db.commit()
    
    def getCurrentActivity(self):
        """Returns the activity that is currently scheduled for the specific lab

        :return: The response from the database containing information about scheduled activity
        :rtype: List
        """
        now = datetime.now() # The current time
        query = "SELECT * FROM lab_schedule WHERE start <= '{}' and end >= '{}'".format(now,now)
        
        self.cursor.execute(query)

        results = self.cursor.fetchall()
        return results
    
    async def markAttendance(self,student_no):
        """Changes status bit from 0 to 1 in the register schema for student with student number student_no

        :param student_no: Student number of student
        :type student_no: String
        """
        results = self.getCurrentActivity()
        for activity in results:
            schedule_id = activity[0]
            query = "UPDATE register SET status = '1' WHERE student_no = '{}' AND schedule_id = '{}';".format(student_no,schedule_id)
            self.cursor.execute(query) 
            self.db.commit()
    
    async def postTempReading(self,student_no,tempValaue):
        """Records the temperature reading from the student in the database

        :param student_no: Student number of student
        :type student_no: String
        :param tempValaue: The temperature reading from student
        :type tempValaue: String
        """
        now = datetime.now()
        now = str(now)[:19]
        temp_id = student_no+"_"+now
        query = "INSERT INTO temperature_log(temp_id,date,temp,student_no) VALUES('{}','{}','{}','{}');".format(temp_id,now,tempValaue,student_no)
        self.cursor.execute(query) 
        self.db.commit()
    
        # print(query)

        # pass

        


# dbObj = database("eee4022sdatabase-do-user-9871310-0.b.db.ondigitalocean.com",
#     "admin",
#     "aGAPX1Hn5TdTE-4I",
#     "lab_system",
#     "25060",
#     "mysql_native_password"
#     )

# results = dbObj.getCurrentActivity()
# dbObj.markAttendance("DXXJOH001")

# results = dbObj.findStudentNumber("DXXJOH001")
# print(results)

# Creating curser
# cursor = db.cursor()
# cursor.execute("SHOW TABLES")

# for table_name in cursor:
#    print(table_name)
    