import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import cv2
import time
from pynput import keyboard

class GestureRecognition:    
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

    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
    VisionRunningMode = mp.tasks.vision.RunningMode

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles


    def __init__(self):
        self.video = cv2.VideoCapture(self.CAM)
        self.current_pressed_key = None
        self.current_gesture = None
        self.gesture_start_time = None
        self.results = None
        self.controller = keyboard.Controller()

        self.options = self.GestureRecognizerOptions(
            base_options=self.BaseOptions(model_asset_path='gesture_recognizer.task'),
            num_hands=2,
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=self.print_result
        )

    def process(self, frame):
        output = frame.copy()
        recognition_result = self.results

        annotated_image = self.visualize(output, recognition_result)

        if recognition_result.gestures:
            top_gesture = max(recognition_result.gestures, key=lambda x: x[0].score)
            if self.current_gesture != top_gesture[0].category_name:
                if self.current_pressed_key:
                    print(f'Releasing: {self.current_pressed_key}')
                    self.controller.release(self.current_pressed_key)
                    self.current_pressed_key = None

                self.current_gesture = top_gesture[0].category_name
                self.gesture_start_time = time.time()
            elif time.time() - self.gesture_start_time >= self.TIME_RECOGNITION and self.current_gesture != "None":
                if self.current_pressed_key is None:
                    print(f"Gesture '{self.current_gesture}' has been maintained for {self.TIME_RECOGNITION} seconds!")
                    gesture_key = self.GESTURES_MAPPED[self.current_gesture]
                    print(f'Pressing: {gesture_key}')
                    self.controller.press(gesture_key)
                    self.current_pressed_key = gesture_key

        else:
            if self.current_pressed_key:
                self.controller.release(self.current_pressed_key)
                self.current_pressed_key = None
            self.current_gesture = None
            self.gesture_start_time = None

        return annotated_image

    def visualize(self, image, recognition_result):
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
                self.mp_drawing.draw_landmarks(
                    image, hand_landmarks_proto, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())

            return image


    def print_result(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        # cv2.imshow('Show', output_image.numpy_view())
        # imright = output_image.numpy_view()

        # print(result.gestures)
        global results
        self.results = result
        # cv2.imwrite('somefile.jpg', imright)
            # ... [additional code if needed] ...

    # def run(self):
    #     timestamp = 0
    #     with self.GestureRecognizer.create_from_options(self.options) as recognizer:
    #         while self.video.isOpened():
    #             ret, frame = self.video.read()

    #             if not ret:
    #                 print("Ignoring empty frame")
    #                 break

    #             timestamp += 1
    #             mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    #             recognizer.recognize_async(mp_image, timestamp)

    #             if self.results:
    #                 frame = self.process(frame)
    #             cv2.imshow('Show', frame)

    #             if cv2.waitKey(1) == ord('q'):
    #                 break

    #     self.video.release()
    #     cv2.destroyAllWindows()


# Usage example
# gesture_recognition = GestureRecognition()
# gesture_recognition.run()
