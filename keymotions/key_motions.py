import time
import json
from typing import List, TypedDict, Literal, Union, Optional, Dict

import cv2
from pynput.keyboard import Key
import mediapipe as mp

from .gesture_recognition import GestureRecognition
from .controller import Controller, KeyInput


class HoldMotion(TypedDict):
    name: Literal["hold"]


class PressMotion(TypedDict):
    name: Literal["press"]
    duration: float


MotionType = Union[HoldMotion, PressMotion]


class Motion(TypedDict):
    name: Literal["✊", "👍", "👎", "✋", "✌️", "🤟", "☝️"]
    value: KeyInput
    motion_type: MotionType
    time_to_press: float


class KeyMotionDict(TypedDict):
    value: KeyInput
    motion_type: MotionType
    time_to_press: float


class KeyMotions:
    NONE_GESTURE = "None"
    HOLD_TYPE = "hold"
    PRESS_TYPE = "press"

    def __init__(self, cam: int = 0, fps: int = 30):
        self.emote_motion_dict = {
            "👍": "Thumb_Up",
            "👎": "Thumb_Down",
            "✊": "Closed_Fist",
            "✋": "Open_Palm",
            "✌️": "Victory",
            "🤟": "ILoveYou",
            "☝️": "Pointing_Up",
        }

        self.motion_key_dict: Dict[str, KeyMotionDict] = {
            "Thumb_Up": {
                "value": Key.up,
                "motion_type": HoldMotion(name=self.HOLD_TYPE),
                "time_to_press": 0.5,
            },
            "Thumb_Down": {
                "value": Key.down,
                "motion_type": HoldMotion(name=self.HOLD_TYPE),
                "time_to_press": 0.5,
            },
            "Closed_Fist": {
                "value": Key.left,
                "motion_type": HoldMotion(name=self.HOLD_TYPE),
                "time_to_press": 0.5,
            },
            "Open_Palm": {
                "value": Key.right,
                "motion_type": HoldMotion(name=self.HOLD_TYPE),
                "time_to_press": 0.5,
            },
            "Victory": {
                "value": "z",
                "motion_type": PressMotion(name=self.PRESS_TYPE, duration=0.5),
                "time_to_press": 0.5,
            },
            "ILoveYou": {
                "value": "x",
                "motion_type": PressMotion(name=self.PRESS_TYPE, duration=0.5),
                "time_to_press": 0.5,
            },
            "Pointing_Up": {
                "value": "a",
                "motion_type": PressMotion(name=self.PRESS_TYPE, duration=0.5),
                "time_to_press": 0.5,
            },
        }

        self.video = None

        self.cam = cam
        self.FPS = fps

        self.current_gesture = None
        self.gesture_start_time = None
        self.gesture_press_time = None

    def run(self):
        gesture_recognizer = GestureRecognition()
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
                    self.handle_gesture(gesture_recognizer, controller, frame)

                cv2.imshow("Show", frame)

                if cv2.waitKey(1) == ord("q"):
                    break

        self.video.release()
        cv2.destroyAllWindows()

    def handle_gesture(self, gesture_recognizer, controller, frame):
        frame, recognition_result = gesture_recognizer.process(frame)

        if recognition_result and recognition_result.gestures:
            top_gesture = max(recognition_result.gestures, key=lambda x: x[0].score)
            gesture_name = top_gesture[0].category_name

            if self.current_gesture != gesture_name:
                if self.current_gesture is not None:
                    controller.release_key()

                self.current_gesture = gesture_name
                self.gesture_start_time = time.time()

            elif self.current_gesture != self.NONE_GESTURE and time.time() - self.gesture_start_time >= self.motion_key_dict[self.current_gesture]["time_to_press"]:
                self.execute_gesture(controller)

    def execute_gesture(self, controller):
        gesture_key = self.motion_key_dict[self.current_gesture]
        if not controller.is_pressing_key():
            print(f"Gesture '{self.current_gesture}' maintained for {gesture_key['time_to_press']} seconds!")
            controller.press_key(gesture_key["value"])
            self.gesture_press_time = time.time()

        elif gesture_key["motion_type"]["name"] == self.PRESS_TYPE and self.gesture_press_time and time.time() - self.gesture_press_time >= gesture_key["motion_type"]["duration"]:
            controller.release_key()
            print(f'Released "{self.current_gesture}" after {gesture_key["motion_type"]["duration"]} seconds!')
            self.reset_gesture()

    def reset_gesture(self):
        self.gesture_press_time = None
        self.current_gesture = None
        self.gesture_start_time = None

    def set_motions(self, motions: List[Motion]):
        for motion in motions:
            motion_name = self.emote_motion_dict[motion["name"]]
            self.motion_key_dict[motion_name] = {
                "value": motion["value"],
                "motion_type": motion["motion_type"],
                "time_to_press": motion["time_to_press"],
            }
        return self

    def set_motions_from_json(self, motions_json):
        with open(motions_json, encoding="utf-8") as json_file:
            motions = json.load(json_file)
        self.set_motions(motions)
        return self
