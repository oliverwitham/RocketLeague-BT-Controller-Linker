# dev code mostly taken from https://pypi.org/project/pyjoystick/
import vgamepad as vg
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
import threading
from queue import Queue
import sys
commands = Queue(maxsize = 1000)
vcontroller = vg.VX360Gamepad()

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

def print_add(joy):
    print('Added', joy)
    # print(joy.identifier)
    print(joy.name)

def print_remove(joy):
    print('Removed', joy)

def key_received(key):
    # if (not commands.empty()):
    #         command = commands.get()
    #         print('Key type: ', command.keytype)
    #         print('Key number: ', command.number)
    #         print('Key raw val: ', command.raw_value)
    #         print('Key number: ', command.number)
    print('key num rx: ', key.number)
    print('key rx type: ', key.is_repeat)
    print('key rx type: ', key.keytype)
    print('key rx raw val: ', key.raw_value)
    print('key rx joy: ', key.joystick)
    print('\n')
    commands.put(key)

def begin_joy_handling():
    run_event_loop(print_add, print_remove, key_received)

def handle_joy_inputs():
    while(1):
        if (not commands.empty()):
            command = commands.get()
            # print('Key type: ', command.keytype)
            # print('Key number: ', command.number)
            # print('Key raw val: ', command.raw_value)
            # print('Key number: ', command.number)
            vcontroller.update()
            if command.keytype == "Button":
                if command.raw_value == 1:
                    try:
                        print('command num: ', command.number)
                        print('pre')
                        print('button_map: ', button_map[command.number], '\n')
                        vcontroller.press_button(button = button_map[command.number])
                    except:
                        # print(command.number)
                        print("error occurred--------------------------")
                else:
                    try:
                        vcontroller.release_button(button = button_map[command.number])
                        vcontroller.update()
                        # vcontroller.release_button(button = button_map[command.number])
                    except:
                        print("error occurred--------------------------")
            vcontroller.update()

joy_input_thread = threading.Thread(target=begin_joy_handling, args=(), daemon=True)
vjoy_handling_thread = threading.Thread(target=handle_joy_inputs, args=(), daemon=True)

vjoy_handling_thread.start()
joy_input_thread.start()

inp = input()
print("Program ended")
sys.exit()