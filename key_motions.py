from typing import List, TypedDict, Literal, Union
from pynput.keyboard import Key
import cv2
from gesture_recognition import GestureRecognition
from controller import Controller, KeyInput
import mediapipe as mp
import time


class Motion(TypedDict):
    name: Literal["✊", "👍", "👎", "✋", "✌️", "🤟", "☝️"]
    value: KeyInput

class KeyMotions:
    def __init__(self):
        self.emote_motion_dict = {
            "👍": "Thumb_Up",
            "👎": "Thumb_Down",
            "✊": "Closed_Fist",
            "✋": "Open_Palm",
            "✌️": "Victory",
            "🤟": "ILoveYou",
            "☝️": "Pointing_Up"
        }

        self.motion_key_dict = {
            "Thumb_Up": Key.up,
            "Thumb_Down": Key.down,
            "Closed_Fist": Key.left,
            "Open_Palm": Key.right,
            "Victory": "z",
            "ILoveYou": "x",
            "Pointing_Up": "a"
        }

        self.recognition_results = None
        self.video = None

        self.cam = 0
        self.FPS = 100
        self.time_recognition = .5

        self.current_gesture = None
        self.gesture_start_time = None

    
    def run(self):
        gesture_recognizer = GestureRecognition(self.cam, self.motion_key_dict)
        controller = Controller()
        self.video = cv2.VideoCapture(self.cam)
        timestamp = 0
        with gesture_recognizer.GestureRecognizer.create_from_options(gesture_recognizer.options) as recognizer:
            while self.video.isOpened():
                ret, frame = self.video.read()

                if not ret:
                    print("Ignoring empty frame")
                    break

                timestamp += 1
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                recognizer.recognize_async(mp_image, timestamp)

                if gesture_recognizer.has_recognized():
                    frame, recognition_result = gesture_recognizer.process(frame)

                    if recognition_result and recognition_result.gestures:
                        top_gesture = max(recognition_result.gestures, key=lambda x: x[0].score)
                        if self.current_gesture != top_gesture[0].category_name:
                            if self.current_gesture is not None:
                                controller.release_key()

                            self.current_gesture = top_gesture[0].category_name
                            self.gesture_start_time = time.time()

                        elif self.gesture_start_time and time.time() - self.gesture_start_time >= self.time_recognition and self.current_gesture != "None":
                            if not controller.is_pressing_key() and self.current_gesture is not None:
                                print(f"Gesture '{self.current_gesture}' has been maintained for {self.time_recognition} seconds!")
                                gesture_key = self.motion_key_dict[self.current_gesture]
                                controller.press_key(gesture_key)
                    else:
                        controller.release_key()
                        self.current_gesture = None
                        self.gesture_start_time = None
                        
                cv2.imshow('Show', frame)

                if cv2.waitKey(1) == ord('q'):
                    break

        self.video.release()
        cv2.destroyAllWindows()

    
    def set_motions(self, motions: List[Motion]):
        for motion in motions:
            motion_name = self.emote_motion_dict[motion["name"]]
            self.motion_key_dict[motion_name] = motion["value"]
        return self


motions_list: List[Motion] = [
    {
        "name":"👍", 
        "value":Key.media_volume_mute
    },
]

motions_list2: List[Motion] = [
    {
        "name":"✊", 
        "value": "d"
    },
]

# key_motions = KeyMotions().set_motions(motions_list).set_motions(motions_list2)
# print(key_motions.motion_key_dict)

k = KeyMotions()
k.run()