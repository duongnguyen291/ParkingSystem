import cv2
import numpy as np
import cvzone
import pickle
import sys

cap = cv2.VideoCapture('easy1.mp4')
drawing = False
area_names = []
try:
    with open("freespace", "rb") as f:
        data = pickle.load(f)
        polylines, area_names = data['polylines'], data['area_names']
except FileNotFoundError:
    polylines = []

points = []
current_name = ""
temp = []
def draw(event, x, y, flags, param):
    global points, drawing, polylines, area_names,temp

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(temp) < 4:  # Only add points if less than 4 points have been selected
            # points.append((x, y))
            temp.append((x,y))
            print(temp)
            print(f"Point added: ({x}, {y})")
        
        if len(temp) == 4:
            drawing = False
            current_name = input('areaname: ')
            if current_name:
                area_names.append(current_name)

                # Calculate intermediate points on lines connecting the selected points
                for i in range(3):
                    start_point = temp[i]
                    end_point = temp[i + 1]
                    num_points = 300  # Number of intermediate points to generate
                    points.append(start_point)
                    for t in np.linspace(0, 1, num_points):
                        x_intermediate = int(start_point[0] + t * (end_point[0] - start_point[0]))
                        y_intermediate = int(start_point[1] + t * (end_point[1] - start_point[1]))
                        print((x_intermediate, y_intermediate))
                        points.append((x_intermediate, y_intermediate))
                    points.append(end_point)

                # Add the polyline to polylines
                print(len(points))
                polylines.append(np.array(points, np.int32))
            temp = []
            points = []  # Clear points for next selection


while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    
    frame = cv2.resize(frame, (1020, 500))
    
    # Draw existing polygons and their names
    for i, polyline in enumerate(polylines):
        cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)
        cvzone.putTextRect(frame, f'{area_names[i]}', tuple(polyline[0]), 1, 1)
    
    cv2.imshow('FRAME', frame)
    cv2.setMouseCallback('FRAME', draw)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # Save current annotations
        with open("freespace", "wb") as f:
            data = {'polylines': polylines, 'area_names': area_names}
            pickle.dump(data, f)
            print("Annotations saved.")
    elif key == ord('q'):
        # Quit the program
        cap.release()
        cv2.destroyAllWindows()
        sys.exit(0)