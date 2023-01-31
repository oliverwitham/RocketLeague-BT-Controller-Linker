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

hat_map = {
    1: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    2: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    4: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    8: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
}

def process_data():
    command = commands.get()
    match command.keytype:
        case "Button":
            if command.raw_value == 1:
                vcontroller.press_button(button = button_map[command.number])
            else:
                vcontroller.release_button(button = button_map[command.number])
        case "Axis":
            print("axis")
        case "Hat":
            print("hat")
            if command.number == 0:
                for i in range(0, 4):
                    vcontroller.release_button(button = hat_map[4])
            elif command.number == 4:
                vcontroller.press_button(button = hat_map[4])
            else:
                pass
        case _:
            print("invalid keytype received")

def update_controller_data():
    pass

def joy_add(joy):
    print('Added', joy)
    print(joy.identifier)
    print(joy.name)

def joy_remove(joy):
    print('Removed', joy)

def joy_key_received(key):
    if key.joystick == "6 axis 15 button gamepad with hat switch":
        commands.put(key)

def begin_joy_handling():
    run_event_loop(joy_add, joy_remove, joy_key_received)

def handle_joy_inputs():
    while(1):
        if (not commands.empty()):
            process_data()
            # update_controller_data()
            vcontroller.update()

# Threads must be daemons so they exit when the main program ends, otherwise the python program won't end
joy_input_thread = threading.Thread(target=begin_joy_handling, args=(), daemon=True)
vjoy_handling_thread = threading.Thread(target=handle_joy_inputs, args=(), daemon=True)

vjoy_handling_thread.start()
joy_input_thread.start()

inp = input()
print("Program ended")
sys.exit()