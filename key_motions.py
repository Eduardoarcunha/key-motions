from typing import List, TypedDict, Literal, Union
from pynput.keyboard import Key
import string
import cv2
from gesture_recognition import *

alphabet = Literal[
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]

class Motion(TypedDict):
    name: Literal["✊", "👍", "👎", "✋", "✌️", "🤟", "☝️"]
    value: Union[alphabet, Key]

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
        self.gesture_recognizer = GestureRecognition()
    
    CAM = 0
    FPS = 100
    WIN = 'Gesture Recognition Example'
    TIME_RECOGNITION = .5

    
    def run(self):
        # De acordo com a taxa de escrita definida pelo usuário
        # Pega leitura do GestureRecognition
        # Escreve valor no teclado de acordo com as moitions definidas
        
        self.video = cv2.VideoCapture(self.CAM)
        timestamp = 0
        with self.gesture_recognizer.GestureRecognizer.create_from_options(self.gesture_recognizer.options) as recognizer:
            while self.video.isOpened():
                ret, frame = self.video.read()

                if not ret:
                    print("Ignoring empty frame")
                    break

                timestamp += 1
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                recognizer.recognize_async(mp_image, timestamp)

                if self.gesture_recognizer.results:
                    frame = self.gesture_recognizer.process(frame)
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