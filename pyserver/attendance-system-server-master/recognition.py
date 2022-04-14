
import cv2 as cv
import numpy as np
import face_recognition
import os
from datetime import datetime
import sqlite3
import time
# import dbcon

time_now = datetime.now()
tStr = time_now.strftime('%H:%M:%S')
dStr = time_now.strftime('%d_%m_%Y')
d=''

ptime = 0
ctime = 0


# conn = sqlite3.connect("../../at.db")
# conn = dbcon.connect()


path = './Image_Folder'
images = []
personNames = []
myList = os.listdir(path)
# print(myList)


for cur_img in myList:
    current_Img = cv.imread(f'{path}/{cur_img}')
    images.append(current_Img)
    personNames.append(os.path.splitext(cur_img)[0])

print(personNames)

def database():
    conn = sqlite3.connect("./attendance.db")
    with conn:   
        cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Class (id TEXT,Name TEXT,Standard TEXT,Time TEXT,Date TEXT)')
    conn.commit()

database()

def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        
        encodeList.append(encode)
    return encodeList


def attendance():
    file_exists = os.path.isfile("Attend"+str(dStr)+".csv")
    if not file_exists:
        f=open("Attend"+str(dStr)+".csv","x")


    with open('Attend'+dStr+'.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            # print(nameList)   

        if id_student not in nameList:
            f.writelines(f'\n{id_student},{name_student},{standard},{tStr},{dStr}') 
            
            conn = sqlite3.connect('./attendance.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Class (id,Name,standard,Time,Date) VALUES(?,?,?,?,?)', (id_student,name_student,standard,tStr,dStr))
            conn.commit()
            d=dStr

encodeListKnown = faceEncodings(images)
print('Encodings Completed')

cap = cv.VideoCapture(0)

while True:

    isTrue, frame = cap.read()
    faces = cv.resize(frame, (0, 0), None, 0.25, 0.25)
    faces = cv.cvtColor(faces, cv.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(faces)
    encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace,tolerance=0.5)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = personNames[matchIndex].upper()
            # print(name)

            # info = name.split('_')
            # class_student = info[0]
            # rollno = info[1]
            # name_student = info[2]
            info = name.split('_')
            id_student = info[0]
            name_student = info[1]
            standard = info[2]
            


            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv.FILLED)
            cv.putText(frame, name_student, (x1 + 6, y2 - 6), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            attendance()

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime 

    cv.putText(frame,str(int(fps)),(10,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)        

    cv.imshow('Webcam', frame)
    if cv.waitKey(1) & 0xFF==ord('e'):
        break

cap.release()
cv.destroyAllWindows()