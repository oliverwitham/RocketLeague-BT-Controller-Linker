import vgamepad as vg
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from queue import Queue
import threading
import time
import sys

vcontroller = vg.VX360Gamepad()

commands = Queue(maxsize = 1000)

# unclear about 10 mapping (should be Select)
button_map = {
    0: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    1: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    3: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    4: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    6: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    7: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    8: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    9: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    10: vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
    11: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
}

hat_dirs = {
    "up": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    "right": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    "down": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    "left": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
}

hat_map = {
    0: [],
    1: [hat_dirs["up"]],
    2: [hat_dirs["right"]],
    3: [hat_dirs["up"], hat_dirs["right"]],
    4: [hat_dirs["down"]],
    6: [hat_dirs["down"], hat_dirs["right"]],
    8: [hat_dirs["left"]],
    9: [hat_dirs["up"], hat_dirs["left"]],
    12: [hat_dirs["down"], hat_dirs["left"]],
}

class JoyFloats:
    x_val: float
    y_val: float
    def __init__(self, x, y):
        self.x_val = float(x)
        self.y_val = float(y)

left_joy = JoyFloats(0, 0)
right_joy = JoyFloats(0, 0)

def updateJoys(command):
    match command.number:
        case 0:
            left_joy.x_val = command.raw_value
            return "left"
        case 1:
            left_joy.y_val = command.raw_value*-1
            return "left"
        case 2:
            pass
        case 3:
            right_joy.x_val = command.raw_value
            return "right"
        case 4:
            right_joy.y_val = command.raw_value
            return "right"
        case 5:
            pass

def hat_handler(command):
    # Release all D-pad buttons
    vcontroller.release_button(button = hat_dirs["up"])
    vcontroller.release_button(button = hat_dirs["right"])
    vcontroller.release_button(button = hat_dirs["down"])
    vcontroller.release_button(button = hat_dirs["left"])

    # Press all buttons for given hat direction
    print("command num: ", command.raw_value),
    print("hat_map: ", hat_map[command.raw_value])
    for btn in hat_map[command.raw_value]:
        vcontroller.press_button(button = btn)

def process_data():
    command = commands.get()
    match command.keytype:
        case "Button":
            if command.raw_value == 1:
                vcontroller.press_button(button = button_map[command.number])
            else:
                vcontroller.release_button(button = button_map[command.number])
        case "Axis":
            dir = updateJoys(command)
            if (dir == "left"):
                vcontroller.left_joystick_float(x_value_float=left_joy.x_val, y_value_float= left_joy.y_val)
            else:
                vcontroller.right_joystick_float(x_value_float=right_joy.x_val, y_value_float=right_joy.y_val)
        case "Hat":
            hat_handler(command)
        case _:
            print("invalid keytype received")

def joy_add(joy):
    print('Added', joy)
    print(joy.identifier)
    print(joy.name)

def joy_remove(joy):
    print('Removed', joy)

def joy_key_received(key):
    if key.joystick == "6 axis 15 button gamepad with hat switch":
        commands.put(key)
        process_data()
        vcontroller.update()

def begin_joy_handling():
    run_event_loop(joy_add, joy_remove, joy_key_received)

# Thread must be a daemon so it exits when the main program ends, otherwise the python program won't end
joy_input_thread = threading.Thread(target=begin_joy_handling, args=(), daemon=True)
joy_input_thread.start()

inp = input()
print("Program ended")
sys.exit()