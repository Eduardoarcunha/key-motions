import cv2 as cv
import numpy as np
import sys
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from matplotlib import pyplot as plt

# Model Path
model_path = 'gesture_recognizer.task'

CAM = 0
FPS = 15
WIN = 'Gesture Recognition Example'

mp_hands = mp.solutions.hands

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Load the model
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.GestureRecognizerOptions(base_options=base_options, num_hands=2)
recognizer = vision.GestureRecognizer.create_from_options(options)

def process(frame):
    output = frame.copy()

    # Convert the frame to mediapipe image format
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=output)

    # Get the recognition result
    recognition_result = recognizer.recognize(mp_image)

    # Annotate the image
    annotated_image = visualize(output, recognition_result)

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
