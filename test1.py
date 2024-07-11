import cv2
import numpy as np
import cvzone
import pickle #lưu các địa điểm khung
import sys

cap = cv2.VideoCapture("easy1.mp4")
area_names = []
drawing = False
try:
    with open("freedom","rb") as f:
            data= pickle.load(f)
            polylines,area_names=data['polylines'],data['area_names'] 
except:
    polylines = []  

points = []
current_name = " "
num = 0
def draw(event, x,y,flags, param):
    global points,drawing,num
    drawing = True
    if event == cv2.EVENT_LBUTTONDOWN:
        points=[(x,y)]
        print((x,y))
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x,y)) 
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False #đánh dấu lại sau khi add vào polylines
        num = num + 1
        current_name= num
        if current_name:
            area_names.append(current_name)
            polylines.append(np.array([points],np.int32))



while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    frame=cv2.resize(frame,(1020,500))
    for i, polyline in enumerate(polylines):
        print(i)
        cv2.polylines(frame,[polyline],True,(0,0,255),2)
        cvzone.putTextRect(frame,f'{area_names[i]}',(polyline[0][0][0], polyline[0][0][1]),1,1)
    cv2.imshow('FRAME', frame)
    cv2.setMouseCallback('FRAME',draw)
    Key = cv2.waitKey(1) & 0xFF
    if Key==ord('s'):
        with open("freedomtech","wb") as f:
            data={'polylines':polylines,'area_names':area_names}
            pickle.dump(data,f)
    if Key==ord('q'):
        cap.release()   
        cv2.destroyAllWindows()
        sys.exit(1)
