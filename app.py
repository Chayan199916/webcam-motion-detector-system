import time
from datetime import datetime

import cv2
import pandas as pd

# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
first_frame = None
start_time = []
end_time = []
status_list = [None, None]
dict = {}

while True:
    check, frame = video.read()
    status = 0
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.GaussianBlur(gray_image, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_image
        continue

    delta_frame = cv2.absdiff(first_frame, gray_image)
    
    thresh_frame = cv2.threshold(delta_frame, 40, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        status = 1
        (x, y, w, z) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + z), (0, 255, 0), 4)
    
    status_list.append(status)
    if status_list[-1] == 1 and status_list[-2] == 0:
        start_time.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        end_time.append(datetime.now())    

    cv2.imshow('Captured Image', frame)
    cv2.imshow('Threshold Image', thresh_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1:
            end_time.append(datetime.now())
        break

dict = {'Start': start_time, 'End': end_time}
df = pd.DataFrame(dict)
df.to_csv('time_stamps.csv')
video.release()
cv2.destroyAllWindows()
