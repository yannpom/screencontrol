#!/usr/bin/env python
import subprocess
import sys
import datetime
from dataclasses import dataclass


@dataclass
class ScreenSettings:
    brightness: float
    gain_red: float
    gain_green: float
    gain_blue: float


SETTINGS = [
    ScreenSettings(brightness=10, gain_red=50, gain_green=10, gain_blue=5),
    ScreenSettings(brightness=100, gain_red=50, gain_green=32, gain_blue=22),
]


def setScreenSettings(brightness, rg, gg, bg):
    print(f"Setting brightness {brightness} with gains {rg} {gg} {bg}")
    print()
    ret = subprocess.run(["ddcctl", "-d", "1", "-b", str(brightness), "-rg", str(rg), "-gg", str(gg), "-bg", str(bg)], capture_output=True)
    print(" ".join(ret.args))
    print()
    sys.stdout.buffer.write(ret.stdout)


def interpolate(i, il, ih, ol, oh):
    if i > ih:
        return oh
    elif i < il:
        return ol
    else:
        ratio = (i-il)/(ih-il)
        return ol + ratio*(oh-ol)


def getGains(brightness):
    return (
        int(interpolate(brightness, SETTINGS[0].brightness, SETTINGS[1].brightness, SETTINGS[0].gain_red, SETTINGS[1].gain_red)),
        int(interpolate(brightness, SETTINGS[0].brightness, SETTINGS[1].brightness, SETTINGS[0].gain_green, SETTINGS[1].gain_green)),
        int(interpolate(brightness, SETTINGS[0].brightness, SETTINGS[1].brightness, SETTINGS[0].gain_blue, SETTINGS[1].gain_blue)),
    )


if len(sys.argv) == 2:
    brightness = int(sys.argv[1])
else:
    print(f"Usage: {sys.argv[0]} [0-100]")
    sys.exit(1)

gain_red, gain_green, gain_blue = getGains(brightness)
setScreenSettings(brightness, gain_red, gain_green, gain_blue)
