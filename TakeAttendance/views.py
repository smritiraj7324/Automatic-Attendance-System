from django.shortcuts import render
from datetime import datetime as dt
#from xmlrpc.client import DateTime
import cv2 as cv
import numpy as np 
import face_recognition as face_rec
import os
from os import listdir
from os.path import isfile,join
import time
from collections import Counter




def resize(img,size):
    width = int(img.shape[1]*size)
    height = int(img.shape[0]*size)
    dimension = (width,height)
    return cv.resize(img,dimension, interpolation= cv.INTER_AREA)

# path = '/home/abhishek/Gui/Attendance/sample_images' 
path = '/home/abhishek/dj/proje/core/static/core/sample_images'

employee_img = [] 
employee_name = []
myList = os.listdir(path)
# print(myList)

for cl in myList:
    curImg = cv.imread(f'{path}/{cl}')  # 'sample_img/img_name.jpg'
    employee_img.append(curImg)
    employee_name.append(os.path.splitext(cl)[0]) #splitting img_name from .jpg






# encoding of imgages
def findEncoding(images):
    encoding_list = [] 
    for img in images:
        img = resize(img,0.50)
        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        encodeimg = face_rec.face_encodings(img)[0]
        encoding_list.append(encodeimg)
    
    return encoding_list 

encode_list = findEncoding(employee_img)

def dateTime():
    date_t = dt.now()
    return str((date_t.strftime("%d/%m/%Y")))





# Attendance capture  
def Attendance(names):
    # with open('/home/abhishek/Gui/Attendance/attendance.csv','r+') as f:
    with open('/home/abhishek/dj/proje/core/static/core/attendance.csv','r+') as f:
        dataList = f.readlines()
        nameList = []
        timeList = []
        # name_time = (dataList[2].split(','))
        # timeList.append(name_time[1].split()[0])
    
        for line in dataList:
            # print(line)      ABHI,01/03/2022 (11:01) in next line Name,Time
            entry = line.split(',')
            nameList.append(entry[0])
            # print('name list of Attendance is ',nameList)
            # print(entry[0])   #['ABHI', '01/03/22 (11:01)']['Name', 'Time\n'] ['\n']
            # timeList.append(entry[1])
            # print(entry)
        
        currTime = dateTime()
        if names not in nameList: #and currTime not in timeList :
            now = dt.now()
            timestr = now.strftime('%d/%m/%y (%H:%M)')
            f.writelines(f'\n{names},{timestr}')
            # tS.say('Welcome to class',name)
            # tS.runAndWait()







def step2_verification(name):
    # loop breaking condintions
    matched = False
    confidenceCounter=0
    end_time1 = time.time() + 0.01*15
    end_time2 = time.time() + 0.50*60

    #while confidenceCounter<10 and time.time() < end_time1:

       
    #-------------------code from other files-----------------------
    # dataPath = name.lower()
    #dataPath = 'Abhishek Kumar'
    pth = '/home/abhishek/dj/pro/TakeAttendance/'
    dataPath = f'{pth}{name.lower()}'
    #print("DATAPath value is:",dataPath)
    # print(dataPath)
    Onlyfiles = [f for f in listdir(dataPath) if isfile(join(dataPath, f))]  # loading all image Samples in form of list
    Training_Data = []
    Labels = []

    for i, files in enumerate(Onlyfiles):  # enumerate provides iteration to no of files present
        imagePath = f"{dataPath}/{Onlyfiles[i]}"  # Onlyfiles[i]
        Images = cv.imread(imagePath, 0)  # cv.IMREAD_GRAYSCALE
        # print(Images)

        td = np.asarray(Images, dtype=np.uint8)  # asarray will create array
        Training_Data.append(td)
        Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)
    # print(Labels) [0,1,2,3....99]
    # print(Training_Data)
    model = cv.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(Training_Data), np.asarray(Labels))  # putting values to LBPHFaceRecognizer_create
    # print("Model has Trained!")

    face_cascade = cv.CascadeClassifier(f"{pth}haarcascade_frontalface_alt.xml")

    # Face detection and camera starts from here

    video = cv.VideoCapture(0)
    #while True:
    while time.time() < end_time2:
        check,frame = video.read()
        grayMode = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grayMode, 1.2, 5)

        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi = frame[y:y + h, x:x + w]  # where face is present
            roi = cv.resize(roi, (200, 200))

        # return img, roi
        try:
            roi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
            result = model.predict(roi)  # sending face for matching with previously stored samples
            # print(result)
            if result[1] < 500:
                confidence = int(100 * (1 - (result[1]) / 300))
                display_string = str(confidence) + "% Confidence it's user"
            cv.putText(frame, display_string, (40, 25), cv.FONT_HERSHEY_COMPLEX, 1, (255, 23, 40), 2)

            if confidence > 84:
                confidenceCounter +=1
                cv.putText(frame, f'{file[0]}', (250, 470), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv.imshow('Face Identity', frame)
            else:
                cv.putText(frame, 'Locked', (250, 470), cv.FONT_HERSHEY_COMPLEX, 1, (255, 20, 255), 2)
                cv.imshow('Face Identity', frame)

        except:
            cv.putText(frame, 'Face Not Found!', (345, 470), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv.imshow('Face Identity', frame)
            pass

        if cv.waitKey(1) == 13 or confidenceCounter == 10:
            matched = True
            break
    if confidenceCounter == 10:
        video.release()
        return matched










def step1_verification():
    vid = cv.VideoCapture(0)
    while True:
        success, frame = vid.read()
        smaller_frames = cv.resize(frame,(0,0),None,0.25,0.25) # 0.25 = 1/4th of image
        frames = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

        faces_in_frame = face_rec.face_locations(smaller_frames)
        encodeFacesInFrames = face_rec.face_encodings(smaller_frames,faces_in_frame)

        #compare faces 
        for encodeFace, faceloc in zip(encodeFacesInFrames,faces_in_frame):
            matches = face_rec.compare_faces(encode_list, encodeFace)
            
            #calculating face-distance
            facedist = face_rec.face_distance(encode_list, encodeFace)
            # print(facedist)
            matchIndex = np.argmin(facedist) #minimum face distance

            if matches[matchIndex]:
                
                name = employee_name[matchIndex].upper()

                names_lst = []
                names_lst.append(name)
                

                y1,x2,y2,x1 = faceloc 
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4 #multiplying each value as it's wrt to smaller frame
                cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
                cv.rectangle(frame,(x1, y2-30),(x2,y2),(0,255,0),cv.FILLED)
                cv.putText(frame,name,(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
                
                Attendance(name)
        cv.imshow('Live Video',frame)
        if cv.waitKey(1) == 13:
            break 
    cv.destroyAllWindows()
    return ''.join(names_lst)


# Create your views here.
def startCameraForAttendance(request):
    
    names = step1_verification()
    context = {'status': 'Status','peoples':names}



    return render(request,'TakeAttendance/startCamera.html',context)
