#!/usr/bin/env python
# coding=utf-8
import sys

from lifxlan import LifxLAN

# Could you please source this file? Also run a linter on it. Overall, great job!
def main():
    number_of_lights = None
    if len(sys.argv) != 2:
        print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
        print("python {} <number of lights on LAN>\n".format(sys.argv[0]))
    else:
        number_of_lights = int(sys.argv[1])

    # instantiate LifexLAN client, number_of_lights may be None (unknown).
    # In fact, you don't need to provide LifexLAN with the number of bulbs at all.
    # lifex = LifexLAN() works just as well. Knowing the number of bulbs in advance
    # simply makes initial bulb discovery faster.
    print("Please Wait - Discovering lights...")
    lifeX = LifxLAN(number_of_lights)

    # get devices
    devices = lifeX.get_lights()
    print("\nFound {} light(s):\n".format(len(devices)))
    for device in devices:
        try:
            print(device)
        except:
            pass

if __name__=="__main__":
    main()
