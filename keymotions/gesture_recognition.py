from typing import Tuple
import os
import pkg_resources


import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2


class GestureRecognition:
    """Class responsible for recognizing gestures and mapping them to key inputs"""

    WIN = "Gesture Recognition Example"

    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
    VisionRunningMode = mp.tasks.vision.RunningMode

    mp_hands = mp.solutions.hands  # type: ignore
    mp_drawing = mp.solutions.drawing_utils  # type: ignore
    mp_drawing_styles = mp.solutions.drawing_styles  # type: ignore

    def __init__(self):
        """Initializes the GestureRecognition class, initializing the video capture and the gesture recognizer"""
        self.results = None

        task_file_path = pkg_resources.resource_filename(
            __name__, "gesture_recognizer.task"
        )

        self.options = self.GestureRecognizerOptions(
            base_options=self.BaseOptions(model_asset_path=task_file_path),
            num_hands=2,
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=self.define_result,
        )

    def define_result(
        self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int
    ):
        """Defines the result of the gesture recognition

        Args:
            result (GestureRecognizerResult): result of the gesture recognition
            output_image (mp.Image): output image
            timestamp_ms (int): timestamp of the result
        """
        self.results = result

    def has_recognized(self) -> bool:
        """Returns if the gesture recognizer has recognized a gesture"""
        return self.results is not None

    def process(self, frame: mp.Image) -> Tuple[mp.Image, GestureRecognizerResult]:
        """Processes the frame and returns the annotated image and the recognition result

        Args:
            frame (mp.Image): frame to be processed

        Returns:
            Tuple[mp.Image, GestureRecognizerResult]: annotated image and recognition result
        """

        output = frame.copy()
        recognition_result = self.results

        annotated_image = self.visualize(output, recognition_result)

        return annotated_image, recognition_result

    def visualize(self, image: mp.Image, recognition_result) -> mp.Image:
        """Return the image annotated with the recognition result

        Args:
            image (mp.Image): image to be visualized
            recognition_result (_type_): recognition result

        Returns:
            mp.Image: annotated image
        """

        if recognition_result.gestures:  # Check if the gestures list is not empty
            y_position = 30  # Starting vertical position for the text
            for gesture in recognition_result.gestures:
                title = f"{gesture[0].category_name} ({gesture[0].score:.2f})"
                cv2.putText(
                    image,
                    title,
                    (10, y_position),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )
                y_position += 40  # Increase vertical position for next gesture
        else:
            cv2.putText(
                image,
                "No gesture detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

        for hand_landmarks in recognition_result.hand_landmarks:
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()  # type: ignore
            hand_landmarks_proto.landmark.extend(
                [
                    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks  # type: ignore
                ]
            )
            self.mp_drawing.draw_landmarks(
                image,
                hand_landmarks_proto,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style(),
            )

        return image


# Usage example
# gesture_recognition = GestureRecognition()
# gesture_recognition.run()
