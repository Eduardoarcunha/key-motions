import cv2 as cv
import numpy as np
import sys
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from matplotlib import pyplot as plt
import time
from pynput import keyboard


# Model Path
model_path = 'gesture_recognizer.task'

CAM = 0
FPS = 15
WIN = 'Gesture Recognition Example'
TIME_RECOGNITION = .5

GESTURES = ["Closed_Fist", "Victory", "Thumb_Up", "Thumb_Down", "Open_Palm", "ILoveYou", "Pointing_Up"]

GESTURES_MAPPED = {
    "Closed_Fist": "a",
    "Victory": "b",
    "Thumb_Up": "c",
    "Thumb_Down": "d",
    "Open_Palm": "e",
    "ILoveYou": "f",
    "Pointing_Up": "g"
}

mp_hands = mp.solutions.hands

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Load the model
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.GestureRecognizerOptions(base_options=base_options, num_hands=2)
recognizer = vision.GestureRecognizer.create_from_options(options)

# Variables to keep track of the current gesture and its start time
current_gesture = None
gesture_start_time = None

controller = keyboard.Controller()

def process(frame):
    global current_gesture, gesture_start_time  # Access the global variables
    
    output = frame.copy()
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=output)
    recognition_result = recognizer.recognize(mp_image)
    annotated_image = visualize(output, recognition_result)

    # Check if gestures are detected
    if recognition_result.gestures:
        # Get the highest scored gesture
        top_gesture = max(recognition_result.gestures, key=lambda x: x[0].score)

        # If it's a new gesture or different from the current gesture, reset the start time
        if current_gesture != top_gesture[0].category_name:
            current_gesture = top_gesture[0].category_name
            gesture_start_time = time.time()
        elif time.time() - gesture_start_time >= TIME_RECOGNITION and current_gesture != "None":  # If the gesture has remained the same for 3 seconds
            print(f"Gesture '{current_gesture}' has remained the same for {TIME_RECOGNITION} seconds!")
            gesture_start_time = time.time()  # Reset the start time to avoid repeated prints
            
            print(f'Pressed: {GESTURES_MAPPED[current_gesture]}')
            controller.press(GESTURES_MAPPED[current_gesture])
            controller.release(GESTURES_MAPPED[current_gesture])

    else:
        current_gesture = None
        gesture_start_time = None

    return annotated_image

def visualize(image, recognition_result):
    """Annotates the image with all gesture categories, their scores, and hand landmarks."""
    
    if recognition_result.gestures:  # Check if the gestures list is not empty
        y_position = 30  # Starting vertical position for the text
        for gesture in recognition_result.gestures:
            title = f"{gesture[0].category_name} ({gesture[0].score:.2f})"
            cv.putText(image, title, (10, y_position), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
            y_position += 40  # Increase vertical position for next gesture
    else:
        cv.putText(image, "No gesture detected", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
    
    for hand_landmarks in recognition_result.hand_landmarks:
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        mp_drawing.draw_landmarks(
            image, hand_landmarks_proto, mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    return image


def main():
    capture = cv.VideoCapture(CAM)
    while True:
        success, frame = capture.read()

        if success:
            annotated_frame = process(frame)
            cv.imshow(WIN, annotated_frame)

        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
