#!/usr/bin/env python3

# /sys/class/backlight/intel_backlight/brightness
# /proc/acpi/button/lid/LID0/state
# setterm -blank 0
import os
import subprocess
import time


class laptop:

    _backlight_file = '/sys/class/backlight/intel_backlight/brightness'
    _lid_file = '/proc/acpi/button/lid/LID0/state'
    _terminal = '/dev/ttyS0'

    def __init__(self, backlight_file=None, lid_file=None, terminal=None):

        if backlight_file is None:
            backlight_file = '/sys/class/backlight/intel_backlight/brightness'
        if not os.path.exists(backlight_file):
            raise FileNotFoundError(f"No backlight file at {backlight_file}")

        if lid_file is None:
            lid_file = '/proc/acpi/button/lid/LID0/state'
        if not os.path.exists(lid_file):
            raise FileNotFoundError(f"No lid file at {lid_file}")

        if terminal is None:
            terminal = '/dev/ttyS0'
        if not os.path.exists(terminal):
            raise FileNotFoundError(f"No console terminal file at {terminal}")

    @property
    def backlight_level(self):
        with open(self._backlight_file, 'r') as f:
            return int(f.readline())

    @backlight_level.setter
    def backlight_level(self, level: int):
        with open(self._backlight_file, 'w') as f:
            f.write(str(level))

    @property
    def lid_state(self):
        with open(self._lid_file, 'r') as f:
            for line in f:
                if 'open' in line:
                    return 'open'
        return 'closed'

    def _do_setterm(self, cmd):
        t = self._terminal
        subprocess.check_output(f"setterm --term linux {cmd} < {t}", shell=True)

    def _poke_terminal(self):
        with open('/sys/class/graphics/fb0/blank','w') as f:
            f.write('0')
        #self._do_setterm('-blank 0')

    @property
    def blank_interval(self):
        t = self._terminal
        value = subprocess.check_output(f'setterm --term linux -blank < {t}', shell=True)
        return int(value)

    @blank_interval.setter
    def blank_interval(self, newval: int):
        self._do_setterm('-blank ' + str(newval))

    def fade_to(self, newlevel, delay=5000):
        orig_level = self.backlight_level
        self._poke_terminal()
        if (orig_level > newlevel):
            step = -1
        else:
            step = 1
        for level in range(orig_level, newlevel, step):
            self.backlight_level = level
            time.sleep(delay / 1000000.0)

    def pulse(self, delay=500):
        orig_level = self.backlight_level
        self._poke_terminal()

        if orig_level < 50:
            newlevel = 100
        else:
            newlevel = 0

        self.fade_to(newlevel, delay=delay)
        self.fade_to(orig_level, delay=delay)

    def blank(self):
        self.blank_interval = 1
        self.backlight_level = 0
