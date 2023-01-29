import vgamepad as vg
import time

vcontroller = vg.VX360Gamepad()

def up_down():
    y_v = 1
    for x in range(0, 2):
        vcontroller.left_joystick_float(x_value_float=0, y_value_float= y_v)
        vcontroller.update()
        y_v *= -1
        time.sleep(0.5)
        vcontroller.left_joystick_float(x_value_float=0, y_value_float= 0)
        vcontroller.update()
        time.sleep(0.5)

while (1):
    vcontroller.press_button(button = vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    vcontroller.update()
    time.sleep(0.1)
    vcontroller.release_button(button = vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    vcontroller.update()
    time.sleep(0.1)
    up_down()
    time.sleep(3)
