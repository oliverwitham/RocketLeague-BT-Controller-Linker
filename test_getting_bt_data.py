# dev code mostly taken from https://pypi.org/project/pyjoystick/

from pyjoystick.sdl2 import Key, Joystick, run_event_loop

def print_add(joy):
    print('Added', joy)
    # print(joy.identifier)
    print(joy.name)

def print_remove(joy):
    print('Removed', joy)

def key_received(key):
    print('Key:', key.keytype)

run_event_loop(print_add, print_remove, key_received)