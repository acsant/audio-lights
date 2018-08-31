#!/usr/bin/env python
# coding=utf-8
import sys
from time import sleep

from lifxlan import BLUE, GREEN, Light


def main():
    bulb = Light("d0:73:d5:28:0b:4a", "10.0.0.16")
    print("Selected {}".format(bulb.get_label()))

    # get original state
    original_power = bulb.get_power()
    original_color = bulb.get_color()
    bulb.set_power("on")

    sleep(0.2) # to look pretty

    print("Toggling power...")
    toggle_device_power(bulb, 0.2)

    print("Toggling color...")
    toggle_light_color(bulb, 0.2)

    # restore original color
    # color can be restored after the power is turned off as well
    print("Restoring original color and power...")
    bulb.set_color(original_color)

    sleep(1) # to look pretty.

    # restore original power
    bulb.set_power(original_power)

def toggle_device_power(device, interval=0.5, num_cycles=3): #TEST
    original_power_state = device.get_power()
    device.set_power("off")
    rapid = True if interval < 1 else False
    for i in range(num_cycles):
        device.set_power("on", rapid)
        sleep(interval)
        device.set_power("off", rapid)
        sleep(interval)
    device.set_power(original_power_state)

def toggle_light_color(light, interval=0.5, num_cycles=3):
    original_color = light.get_color()
    rapid = True if interval < 1 else False
    for i in range(num_cycles):
        light.set_color(BLUE, rapid=rapid)
        sleep(interval)
        light.set_color(GREEN, rapid=rapid)
        sleep(interval)
    light.set_color(original_color)

if __name__=="__main__":
    main()
