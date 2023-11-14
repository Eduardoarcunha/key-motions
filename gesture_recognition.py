import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import cv2


class GestureRecognition:    
    WIN = 'Gesture Recognition Example'

    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
    VisionRunningMode = mp.tasks.vision.RunningMode

    mp_hands = mp.solutions.hands # type: ignore
    mp_drawing = mp.solutions.drawing_utils # type: ignore
    mp_drawing_styles = mp.solutions.drawing_styles # type: ignore


    def __init__(self, cam, motion_key_dict):
        self.video = cv2.VideoCapture(cam)
        self.results = None
        self.motion_key_dict = motion_key_dict

        self.options = self.GestureRecognizerOptions(
            base_options=self.BaseOptions(model_asset_path='gesture_recognizer.task'),
            num_hands=2,
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=self.define_result
        )

    
    def define_result(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        self.results = result

    def has_recognized(self) -> bool:
        return self.results is not None

    def process(self, frame):
        output = frame.copy()
        recognition_result = self.results

        annotated_image = self.visualize(output, recognition_result)

        return annotated_image, recognition_result

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
                hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList() # type: ignore
                hand_landmarks_proto.landmark.extend([
                    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks # type: ignore
                ])
                self.mp_drawing.draw_landmarks(
                    image, hand_landmarks_proto, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())

            return image

# Usage example
# gesture_recognition = GestureRecognition()
# gesture_recognition.run()