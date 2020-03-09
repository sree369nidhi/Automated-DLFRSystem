import cv2,os
import time
import sqlite3
import numpy as np
from PIL import Image
import datetime


def RegisterEmployee():
    vid = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    if not os.path.exists('./dataset'):
        os.makedirs('./dataset')

    print("Enter your details for Face Recognition")

    conn = sqlite3.connect('Students.db')
    db = conn.cursor()

    mobile = input("Mobile NO. : ")
    name = input("Name :")
    email = input("EMail : ")

    dirpath = './dataset/' + name + " " + mobile
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    name = name.replace(" ", '_')

    sql_cmd = '''CREATE TABLE IF NOT EXISTS Students (Mobile integer PRIMARY KEY NOT NULL UNIQUE, Name text, Email text)'''
    db.execute(sql_cmd)

    if mobile and name and email:
        try:
            sql_cmd = "INSERT INTO Students values(?,?,?)"
            db.execute(sql_cmd, [(mobile), (str(name)), (str(email))])

            sql_cmd = '''CREATE TABLE IF NOT EXISTS {}(Date text PRIMARY KEY NOT NULL UNIQUE,
                                            Login text, Logout text, TimeDelta text, TimedOut text)'''.format(name + '_' +str(mobile))
            db.execute(sql_cmd)

            Cntr = 0
            Name = name.replace("_", ' ')

            while (True):
                ret, img = vid.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    time.sleep(0.5)
                    Cntr = Cntr + 1
                    cv2.imwrite("dataset/"+ Name + ' ' + mobile + "/" + Name + 'LiveCapture' + str(Cntr) + ".jpg", gray[y:y + h, x:x + w])
                    cv2.imshow('frame', img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif Cntr > 11:
                    break

            vid.release()
            cv2.destroyAllWindows()
            time.sleep(1)

            conn.commit()
            conn.close()

            print("Thankyou for Registering...Process in progress")

            os.system("python extract_embeddings.py --dataset dataset --embeddings output/embeddings.pickle --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7")
            print("Successfully Embeddings are extracted from the dataset...")

            os.system("python train_model.py --embeddings output/embeddings.pickle --recognizer output/recognizer.pickle --le output/le.pickle")
            print("Successfully Re-Trained the Model on Embeddings extracted from the dataset...")
            
        except Exception as e:
            print('Mobile No Already Exists...Proceed to Login directly')
    else:
        print("Mobile Number, Name, Email are mandatory  fields can't be blank... Please enter to proceed")


RegisterEmployee()