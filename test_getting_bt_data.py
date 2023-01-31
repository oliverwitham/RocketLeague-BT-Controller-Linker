# dev code mostly taken from https://pypi.org/project/pyjoystick/

from pyjoystick.sdl2 import Key, Joystick, run_event_loop

def print_add(joy):
    print('Added', joy)
    # print(joy.identifier)
    print(joy.name)

def print_remove(joy):
    print('Removed', joy)

def key_received(key):
    print('Key type: ', key.keytype)
    print('Key number: ', key.number)
    print('Key raw val: ', key.raw_value)
    print('Key number: ', key.number)


run_event_loop(print_add, print_remove, key_received)