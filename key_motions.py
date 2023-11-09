from typing import List, TypedDict, Literal, Union
from pynput.keyboard import Key
import string

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

    
    def run(self):
        return
    
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

key_motions = KeyMotions().set_motions(motions_list).set_motions(motions_list2)

print(key_motions.motion_key_dict)