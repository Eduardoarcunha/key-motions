from pynput import keyboard
from pynput.keyboard import Key
from typing import Literal, Union, Optional

alphabet = Literal[
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]

KeyInput = Union[alphabet, Key]

class Controller:
    """
    Class responsible for writing inputs into the keyboard

    Atributes:
        current_pressed_key (Optional[Union[alphabet, Key]]) : state of the current key being pressed
        controller (pynput.keyboard.Controller) : external dependency responsible for handling keyboard inputs
    """

    current_pressed_key: Optional[KeyInput]
    controller: keyboard.Controller
    
    def __init__(self) -> None:
        """
        Initializes class, creating controller atribute and defining current_pressed_key as None
        """
        
        self.current_pressed_key = None
        self.controller = keyboard.Controller()

    def press_key(self, key: KeyInput) -> None:
        """Press the key

        Args:
            key (Union[alphabet, Key]): Value of the key that is going to be pressed
        """   

        print(f'Pressing: {key}')
        self.controller.press(key)
        self.current_pressed_key = key


    def release_key(self) -> None:
        """Release the current pressed key by the controller
        """        
        
        if self.current_pressed_key:
            print(f'Releasing: {self.current_pressed_key}')
            self.controller.release(self.current_pressed_key)
            self.current_pressed_key = None
        

    def is_pressing_key(self) -> bool:
        """Returns if controller is pressing a key

        Returns:
            bool: True if controller is currently pressing a key, False if it is not pressing
        """    
            
        return self.current_pressed_key is not None