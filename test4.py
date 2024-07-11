import cv2
import numpy as np
import pickle
import pandas as pd
from ultralytics import YOLO
import cvzone
import sys
from tkinter import *
from PIL import Image, ImageTk
from playsound import playsound

# Load model and data
with open("freespace", "rb") as f:
    data = pickle.load(f)
    polylines, area_names = data['polylines'], data['area_names']

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

model = YOLO('yolov8s.pt')

cap = cv2.VideoCapture('easy1.mp4')

count = 0
prev_car_count = 0  # Variable to store the previous car count

# Tkinter GUI setup
root = Tk()
root.title("Parking System")
root.geometry("1280x720")

# Create frames
left_frame = Frame(root, width=1020, height=500)
left_frame.grid(row=0, column=0, padx=10, pady=10)

right_frame = Frame(root, width=250, height=500)
right_frame.grid(row=0, column=1, padx=10, pady=10)

# Labels for displaying information
car_count_label = Label(right_frame, text="CAR COUNTER: 0", font=("Helvetica", 16))
car_count_label.pack(pady=20)

freespace_label = Label(right_frame, text="FREESPACE: 0", font=("Helvetica", 16))
freespace_label.pack(pady=20)

# Quit button
def quit_program():
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()
    sys.exit(1)

quit_button = Button(right_frame, text="Quit", command=quit_program, font=("Helvetica", 16))
quit_button.pack(pady=20)

# Label for video frame
video_label = Label(left_frame)
video_label.pack()

def update_frame():
    global count, prev_car_count
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return
   
    count += 1
    if count % 3 != 0:
        root.after(10, update_frame)
        return

    frame = cv2.resize(frame, (1020, 500))
    frame_copy = frame.copy()
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    list1 = []
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        
        c = class_list[d]
        cx = int(x1 + x2) // 2
        cy = int(y1 + y2) // 2
        if 'car' in c:
            list1.append([cx, cy])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2) # Draw car rectangles

    counter1 = []
    list2 = []
    for i, polyline in enumerate(polylines):
        list2.append(i)
        cv2.polylines(frame, [polyline], True, (0, 255, 0), 2)
        cvzone.putTextRect(frame, f'{area_names[i]}', (polyline[0][0], polyline[0][1]), 1, 1)
        for i1 in list1:
            cx1 = i1[0]
            cy1 = i1[1]
            cv2.circle(frame, (cx1, cy1), 5, (255, 0, 0), -1)
            results = cv2.pointPolygonTest(polyline, (cx1, cy1), False)
            if results >= 0:
                cv2.circle(frame, (cx1, cy1), 5, (255, 0, 0), -1)
                cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)
                counter1.append(cx1)
                
    car_count = len(counter1)
    free_space = len(list2) - car_count

    # Play sound if car count changes
    if car_count > prev_car_count:
        playsound(r'D:\code\Test\parking_system\car_in.mp3')
    elif car_count < prev_car_count:
        playsound(r'D:\code\Test\parking_system\car_out.mp3')
    prev_car_count = car_count

    car_count_label.config(text=f"CAR COUNTER: {car_count}")
    freespace_label.config(text=f"FREESPACE: {free_space}")

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    video_label.config(image=img)
    video_label.image = img

    root.after(10, update_frame)

# Start the video frame update loop
update_frame()

# Run the Tkinter main loop
root.mainloop()
