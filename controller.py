from pynput import keyboard

class Controller:

    def __init__(self) -> None:
        self.current_pressed_key = None
        self.controller = keyboard.Controller()

    def press_key(self, key):
        print(f'Pressing: {key}')
        self.controller.press(key)
        self.current_pressed_key = key


    def release_key(self):
        if self.current_pressed_key:
            print(f'Releasing: {self.current_pressed_key}')
            self.controller.release(self.current_pressed_key)
            self.current_pressed_key = None
        

    def is_pressing_key(self) -> bool:
        return self.current_pressed_key is not None

            

    # def control_key(self, should_press, delta_time, motion_key_dict, is_changing_key):
    #     if gestures:
    #         top_gesture = max(gestures, key=lambda x: x[0].score)       # Press onde the gesture with the highest score
    #         if self.current_gesture != top_gesture[0].category_name:
    #             if self.current_pressed_key:
    #                 self.controller.release(self.current_pressed_key)
    #                 self.current_pressed_key = None
    #                 print(f'Releasing: {self.current_pressed_key}')

    #             self.current_gesture = top_gesture[0].category_name
    #             self.gesture_start_time = time.time()
                
    #         elif time.time() - self.gesture_start_time >= delta_time and self.current_gesture != "None":
    #             if self.current_pressed_key is None:
                    
    #     else:
    #         if self.current_pressed_key:
    #             self.controller.release(self.current_pressed_key)
    #             self.current_pressed_key = None
    #         self.current_gesture = None
    #         self.gesture_start_time = None