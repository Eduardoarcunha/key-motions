from typing import List, TypedDict, Literal, Union, Optional, Dict
from gesture_recognition import GestureRecognition
from controller import Controller, KeyInput
from pynput.keyboard import Key
import mediapipe as mp
import time
import cv2


class HoldMotion(TypedDict):
    name: Literal["hold"]


class PressMotion(TypedDict):
    name: Literal["press"]
    duration: float


class Motion(TypedDict):
    name: Literal["✊", "👍", "👎", "✋", "✌️", "🤟", "☝️"]
    value: KeyInput
    motion_type: Union[HoldMotion, PressMotion]
    time_to_press: float


class KeyMotionDict(TypedDict):
    value: KeyInput
    motion_type: Union[HoldMotion, PressMotion]
    time_to_press: float


class KeyMotions:
    def __init__(self):
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
                "motion_type": PressMotion(name="press", duration=2),
                "time_to_press": 5,
            },
            "Thumb_Down": {
                "value": Key.down,
                "motion_type": HoldMotion(name="hold"),
                "time_to_press": 0.5,
            },
            "Closed_Fist": {
                "value": Key.left,
                "motion_type": HoldMotion(name="hold"),
                "time_to_press": 0.5,
            },
            "Open_Palm": {
                "value": Key.right,
                "motion_type": HoldMotion(name="hold"),
                "time_to_press": 0.5,
            },
            "Victory": {
                "value": "z",
                "motion_type": HoldMotion(name="hold"),
                "time_to_press": 0.5,
            },
            "ILoveYou": {
                "value": "x",
                "motion_type": HoldMotion(name="hold"),
                "time_to_press": 0.5,
            },
            "Pointing_Up": {
                "value": "a",
                "motion_type": HoldMotion(name="hold"),
                "time_to_press": 0.5,
            },
        }

        self.recognition_results = None
        self.video = None

        self.cam = 0
        self.FPS = 100
        self.time_recognition = 0.5

        self.current_gesture = None
        self.gesture_start_time = None
        self.gesture_press_time = None

    def run(self):
        gesture_recognizer = GestureRecognition()
        controller = Controller()
        self.video = cv2.VideoCapture(self.cam)
        timestamp = 0
        with gesture_recognizer.GestureRecognizer.create_from_options(
            gesture_recognizer.options
        ) as recognizer:
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
                        top_gesture = max(
                            recognition_result.gestures, key=lambda x: x[0].score
                        )
                        if self.current_gesture != top_gesture[0].category_name:
                            if self.current_gesture is not None:
                                controller.release_key()

                            self.current_gesture = top_gesture[0].category_name
                            self.gesture_start_time = time.time()

                        elif (
                            self.current_gesture is not None
                            and self.current_gesture != "None"
                            and self.gesture_start_time
                            and time.time() - self.gesture_start_time
                            >= self.motion_key_dict[self.current_gesture][
                                "time_to_press"
                            ]
                        ):
                            if not controller.is_pressing_key():
                                print(
                                    f"Gesture '{self.current_gesture}' has been maintained for {self.motion_key_dict[self.current_gesture]['time_to_press']} seconds!"
                                )
                                gesture_key = self.motion_key_dict[self.current_gesture]
                                controller.press_key(gesture_key["value"])
                                self.gesture_press_time = time.time()

                            elif (
                                self.motion_key_dict[self.current_gesture][
                                    "motion_type"
                                ]["name"]
                                == "press"
                                and self.gesture_press_time
                                and time.time() - self.gesture_press_time
                                >= self.motion_key_dict[self.current_gesture][
                                    "motion_type"
                                ][
                                    "duration"
                                ]  # type: ignore
                            ):
                                controller.release_key()
                                print(
                                    f'Released "{self.current_gesture}" after {self.motion_key_dict[self.current_gesture]["motion_type"]["duration"]} seconds!'  # type: ignore
                                )
                                self.gesture_press_time = None
                                self.current_gesture = None
                                self.gesture_start_time = None

                    else:
                        controller.release_key()
                        self.current_gesture = None
                        self.gesture_start_time = None

                cv2.imshow("Show", frame)

                if cv2.waitKey(1) == ord("q"):
                    break

        self.video.release()
        cv2.destroyAllWindows()

    def set_motions(self, motions: List[Motion]):
        for motion in motions:
            motion_name = self.emote_motion_dict[motion["name"]]
            self.motion_key_dict[motion_name] = {
                "value": motion["value"],
                "motion_type": motion["motion_type"],
                "time_to_press": motion["time_to_press"],
            }
        return self


motions_list: List[Motion] = [
    {
        "name": "👍",
        "value": "a",
        "motion_type": HoldMotion(name="hold"),
        "time_to_press": 0.5,
    }
]

motions_list2: List[Motion] = [
    {
        "name": "✊",
        "value": "d",
        "motion_type": PressMotion(name="press", duration=1),
        "time_to_press": 0.5,
    },
]

# key_motions = KeyMotions().set_motions(motions_list).set_motions(motions_list2)
# print(key_motions.motion_key_dict)

k = KeyMotions()
k.run()
