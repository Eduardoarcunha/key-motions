import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import cv2
import time
from pynput import keyboard


CAM = 0
FPS = 100
WIN = 'Gesture Recognition Example'
TIME_RECOGNITION = .5

GESTURES = ["Closed_Fist", "Victory", "Thumb_Up", "Thumb_Down", "Open_Palm", "ILoveYou", "Pointing_Up"]

GESTURES_MAPPED = {
    "Closed_Fist": "a",
    "Victory": keyboard.Key.left,
    "Thumb_Up": keyboard.Key.up,
    "Thumb_Down": keyboard.Key.down,
    "Open_Palm": keyboard.Key.right,
    "ILoveYou": "z",
    "Pointing_Up": "g"
}

current_gesture = None
gesture_start_time = None

controller = keyboard.Controller()

results = None

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


video = cv2.VideoCapture(CAM)

def process(frame):
    global current_gesture, gesture_start_time  # Access the global variables
    
    output = frame.copy()
    # mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=output)
    # recognition_result = recognizer.recognize(mp_image)
    
    global results
    recognition_result = results

    annotated_image = visualize(output, recognition_result)

    # Check if gestures are detected
    if recognition_result.gestures:
        # Get the highest scored gesture
        top_gesture = max(recognition_result.gestures, key=lambda x: x[0].score)

        # If it's a new gesture or different from the current gesture, reset the start timeeeee
        if current_gesture != top_gesture[0].category_name:
            current_gesture = top_gesture[0].category_name
            gesture_start_time = time.time()
        elif time.time() - gesture_start_time >= TIME_RECOGNITION and current_gesture != "None":  # If the gesture has remained the same for 3 seconds
            print(f"Gesture '{current_gesture}' has remained the same for {TIME_RECOGNITION} seconds!")
            gesture_start_time = time.time()  # Reset the start time to avoid repeated prints
            
            print(f'Pressed: {GESTURES_MAPPED[current_gesture]}')
            controller.press(GESTURES_MAPPED[current_gesture])
            # time.sleep(1)
            # controller.release(GESTURES_MAPPED[current_gesture])

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
            cv2.putText(image, title, (10, y_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            y_position += 40  # Increase vertical position for next gesture
    else:
        cv2.putText(image, "No gesture detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
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

# Create a image segmenter instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    # cv2.imshow('Show', output_image.numpy_view())
    # imright = output_image.numpy_view()

    # print(result.gestures)
    global results
    results = result
    # cv2.imwrite('somefile.jpg', imright)


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    num_hands=2,
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

timestamp = 0
with GestureRecognizer.create_from_options(options) as recognizer:
  # The recognizer is initialized. Use it here.
    while video.isOpened(): 
        # Capture frame-by-frame
        ret, frame = video.read()

        if not ret:
            print("Ignoring empty frame")
            break

        timestamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Send live image data to perform gesture recognition
        # The results are accessible via the `result_callback` provided in
        # the `GestureRecognizerOptions` object.
        # The gesture recognizer must be created with the live stream mode.
        recognizer.recognize_async(mp_image, timestamp)
        # if results: print(results.gestures)
        if results:
            frame = process(frame)
        cv2.imshow('Show', frame)

        # delay = round(1000 / FPS)
        if cv2.waitKey(1) == ord('q'):
            break

video.release()
cv2.destroyAllWindows()