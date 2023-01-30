import vgamepad as vg
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from queue import Queue
import threading
import time
import sys

vcontroller = vg.VX360Gamepad()

commands = Queue(maxsize = 1000)

def process_data():
    print("processing")
    command = commands.get()
    print(command)

def update_controller_data():
    print("updating controller data")
    # vcontroller.

def joy_add(joy):
    print('Added', joy)
    print(joy.identifier)
    print(joy.name)

def joy_remove(joy):
    print('Removed', joy)

def joy_key_received(key):
    print('Key:', key)
    commands.put(key)

def begin_joy_handling():
    run_event_loop(joy_add, joy_remove, joy_key_received)

def handle_joy_inputs():
    while(1):
        if (not commands.empty()):
            process_data()
            update_controller_data()
            vcontroller.update()

# Threads must be daemons so they exit when the main program ends, otherwise the python program won't end
joy_input_thread = threading.Thread(target=begin_joy_handling, args=(), daemon=True)
vjoy_handling_thread = threading.Thread(target=handle_joy_inputs, args=(), daemon=True)

vjoy_handling_thread.start()
joy_input_thread.start()

inp = input()
print("Program ended")
sys.exit()