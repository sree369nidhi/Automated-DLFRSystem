import cv2
import numpy as np
import sqlite3
import datetime
from recognize_func import FaceRecognition


def Login():

    conn = sqlite3.connect('Students.db')
    db = conn.cursor()

    # NOTE: input mobile which is already Registered in previous page
    mobile_no = input("Enter mobile NO: ")

    if mobile_no:
        try:
            sql = """SELECT * from Students WHERE Mobile = ?"""
            db.execute(sql, [(mobile_no)])
            rows = db.fetchone()
            if rows:
                if mobile_no == str(rows[0]):
                    name = FaceRecognition()
                    print("Name:", name)
                    EmpTable = str(rows[1]).replace("_", " ") + " " + str(rows[0])
                    print('EmpTable :', EmpTable)
                    print(name == EmpTable)
                    if name == EmpTable:
                        name = name.replace(" ", '_')
                        print("name",name)
                        try:
                            sql = """SELECT Date, Login from {} WHERE Date = ?""".format(name)
                            db.execute(sql, [(str(datetime.date.today()))])
                            row = db.fetchone()

                            if row == None:
                                sql = """INSERT INTO {} (Date, Login)values(?, ?)""".format(name)
                                db.execute(sql, [(str(datetime.date.today())) ,(str(datetime.datetime.now()))])
                                conn.commit()
                                print('Login Successful date on {} and login at {} recorded'.format(str(datetime.date.today()), str(datetime.datetime.now())))
                            else:
                                print("You have already logged in today...Can't login twice in a same day")
                        except Exception as e:
                            print("Database retrieval Error...Please try again")
        except Exception as e:
                    print('Database retrieval error...Or Number is blank')
    else:
        print('Please enter mobile No.')

    conn.commit()
    conn.close()


Login()
