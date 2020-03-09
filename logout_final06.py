import cv2
import numpy as np
import sqlite3
import datetime
from recognize_func import FaceRecognition
from AUTOMATED_EMAIL_FINAL import sendAutomatedMail

def Logout():

    conn = sqlite3.connect('Students.db')
    db = conn.cursor()

    now_time = datetime.datetime.now()
    end = datetime.datetime(now_time.year, now_time.month, now_time.day, 17, 0, 0)

    if now_time >= end:
        sql = """SELECT * from Students"""
        db.execute(sql)
        rows = db.fetchall()
        for Srow in rows:

            mobile_no = Srow[0]
            EmpTable = str(Srow[1]) + "_" + str(Srow[0])
            sql = """SELECT Date, Login, Logout, TimeDelta, TimedOut from {} WHERE Date = ?""".format(EmpTable)
            db.execute(sql, [(str(datetime.date.today()))])
            row = db.fetchone()

            if row:
                if row[2] == None and row[3] == None and row[4] == None:

                    date = row[0]
                    login = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
                    logout = end
                    timeDelta = logout - login
                    min = timeDelta.total_seconds()/60.0
                    sql = """UPDATE {} set Logout = ?, TimeDelta = ?, TimedOut = ?""".format(EmpTable)
                    db.execute(sql, [(str(end)), str(min), ('True')])
                    conn.commit()
                    # NOTE: Code for AutomatedEmail is called through fuction for modularity
                    name = Srow[1]
                    email_address = Srow[2]
                    print(name, email_address)
                    try:
                        sendAutomatedMail(name=name, email_address=email_address)
                        print('Automatic Mail has been sent...')
                    except Exception as e:
                        print('No internet service for sending email...')

    elif now_time < end:
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
                        print("Name : ", name)
                        Name = rows[1].replace("_"," ")
                        EmpTable = str(Name) + " " +str(rows[0])
                        print(EmpTable)
                        if EmpTable == name:
                            name = name.replace(" ","_")
                            try:
                                sql = """SELECT Logout from {} WHERE Date = ?""".format(name)
                                db.execute(sql, [(str(datetime.date.today()))])
                                row = db.fetchone()
                                if row[0] == None:
                                    print(f"{Name} hasn't Logged out yet, Proceeding to Logout")

                                    sql = """UPDATE {} SET Logout = ?""".format(name)
                                    db.execute(sql, [(str(datetime.datetime.now()))])
                                    conn.commit()

                                    sql = """SELECT Date, Login, Logout, TimeDelta, TimedOut from {} WHERE Date = ?""".format(name)
                                    db.execute(sql,[(str(datetime.date.today()))])
                                    row = db.fetchone()
                                    if row:
                                        date = row[0]
                                        login = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
                                        logout = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
                                        timeDelta = logout - login
                                        min = timeDelta.total_seconds()/60.0
                                        if row[3] == None and row[4] == None:
                                            print(f"Saving total time spent by {Name} Employee on Date {date}...")
                                            sql = """UPDATE {} SET timeDelta = ?, TimedOut = ?""".format(name)
                                            db.execute(sql, [(str(min)), ('False')])
                                            conn.commit()
                                            print(f"{Name} Employee total time spent in office on Date {date} is : {timeDelta} or {min} Minutes")
                                            print(f"{Name} your Logout Successful...Data has been saved successfully...Thank you for your service...Have a nice day")

                                else:
                                    print(f'{Name} Employee is Already successfully logged out and data has been saved...')
                            except Exception as e:
                                print("User doesn't exist...or Database retrieval error")
                        else:
                            print("User doesn't exist...Please register first or Wrong person identified i.e: person and mobile number mismatch")

            except Exception as e:
                print("User doesn't exist...or Database retrieval error")
        else:
            print("Please enter mobile No. It can't be blank")

    conn.commit()
    conn.close()

Logout()
