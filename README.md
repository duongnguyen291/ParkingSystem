# Parking System Vehicle Detection

## Overview

This project is a vehicle detection system designed for monitoring parking spaces. The system uses the YOLO (You Only Look Once) model for object detection, specifically trained to identify cars. It provides a graphical user interface (GUI) using Tkinter to display real-time video feed, count the number of cars, and calculate the available free spaces.

## Features

- **Real-time Video Feed**: Displays the video feed from a video file.
- **Car Detection**: Uses the YOLO model to detect cars in the video feed.
- **Parking Space Monitoring**: Calculates the number of occupied and free parking spaces.
- **Sound Alerts**: Plays sound alerts when a car enters or leaves a parking space.
- **User Interface**: A Tkinter-based GUI to show the video feed, car count, and free spaces.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- Pandas
- Tkinter
- PIL (Pillow)
- Playsound
- YOLOv8 model from Ultralytics
- Predefined polylines and area names for parking spaces

## Setup Instructions

1. **Clone the repository** (if applicable):
   ```bash
   git clone [<repository_url>](https://github.com/duongnguyen291/ParkingSystem/)
   cd  [<repository_url>](https://github.com/duongnguyen291/ParkingSystem/)
   ```

2. **Install the required Python packages**:
   ```bash
   pip install opencv-python-headless numpy pandas pillow playsound ultralytics
   ```

3. **Prepare the necessary files**:
   - `freespace`: A pickle file containing predefined polylines and area names for the parking spaces.
   - `coco.txt`: A file containing the list of class names used by the YOLO model.
   - `yolov8s.pt`: The YOLOv8 model file.
   - `easy1.mp4`: A video file to be used for car detection.

4. **Ensure the sound files for alerts are available**:
   - `car_in.mp3`: Sound file played when a car enters a parking space.
   - `car_out.mp3`: Sound file played when a car leaves a parking space.

## Running the Application

1. **Execute the Python script**:
   ```bash
   python parking_system.py
   ```

2. **GUI Interface**:
   - The left side of the interface displays the video feed with detected cars and parking spaces.
   - The right side shows the car count and the number of free spaces.
   - A "Quit" button is provided to exit the application.

## Script Breakdown

### Loading Model and Data
- Loads the YOLO model and predefined parking space data from pickle and text files.

### Tkinter GUI Setup
- Sets up the main application window and layout with frames and labels for displaying information.

### Video Frame Update
- Continuously captures frames from the video feed, detects cars, and updates the GUI with the current car count and free spaces.
- Plays sound alerts if the car count changes.

### Event Loop
- The `update_frame` function is called in a loop to keep the video feed and GUI updated.

## License

This project is licensed under the MIT License.

## Acknowledgements

- **YOLO**: The YOLO model by Ultralytics for its powerful real-time object detection capabilities.
- **OpenCV**: For providing robust computer vision tools.
- **Tkinter**: For the GUI framework.
- **Playsound**: For handling audio alerts.

For any further questions or issues, please refer to the repository or contact the project maintainers.

---
