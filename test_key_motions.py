from pynput.keyboard import Key
from keymotions import KeyMotions
from keymotions.key_motions import HoldMotion, PressMotion

def test_set_motions():
    key_motions = KeyMotions()

    motions = [
        {
            "name": "👍",
            "value": Key.up,
            "motion_type": HoldMotion(name="hold"),
            "time_to_press": 1.0,
        },
        {
            "name": "✌️",
            "value": "z",
            "motion_type": PressMotion(name="press", duration=0.5),
            "time_to_press": 0.5,
        },
    ]

    key_motions.set_motions(motions)

    assert key_motions.motion_key_dict["Thumb_Up"] == {
        "value": Key.up,
        "motion_type": {"name": "hold"},
        "time_to_press": 1.0,
    }

    assert key_motions.motion_key_dict["Victory"] == {
        "value": "z",
        "motion_type": {"name": "press", "duration": 0.5},
        "time_to_press": 0.5,
    }
