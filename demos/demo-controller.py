from pynput import keyboard, mouse

def on_press(key):
    try:
        print(f'Pressed: {key.char}')
        if key.char == 'g':
            print('g pressed')
            with mouse.Controller() as controller:
                controller.click(mouse.Button.left)
    except AttributeError:
        pass

    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
