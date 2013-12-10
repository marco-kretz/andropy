#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import subprocess
from os.path import expanduser, isfile


ADB_DEV_PATTERN = re.compile("^[A-Z0-9]{12}\sdevice$")
ADB_EXE = expanduser("~") + "/.andropy/bin/adb"

class ADBInterface():
    """
    Simple interface for working with ADB.
    """
    def __init__(self):
        if not isfile(ADB_EXE):
            sys.exit("No ADB binary has been found.\n" + \
                     "Please run the Installer first.")
        subprocess.check_output([ADB_EXE, "start-server"])

    def __enter__(self):
        if len(self.get_devices()) > 0:
            return self
        sys.exit("No devices found.")

    def get_devices(self):
        """
        Return a list containing all connected ADB-devices.
        """
        devices = []
        out = subprocess.check_output([ADB_EXE, "devices"],
                                      universal_newlines=True)
        self.check_output(out)
        for line in out.split('\n'):
            if ADB_DEV_PATTERN.match(line):
                devices.append(line[:12])
        return devices

    def exec_shell_cmd(self, cmd, output=True):
        """
        Exec a shell command via ADB, select wether output is returned or not.
        Return a list of output-lines.
        """
        response = []
        out = subprocess.check_output([ADB_EXE, "shell", cmd],
                                      universal_newlines=True)
        self.check_output(out)
        for line in out.split('\n'):
            if line == '':
                continue
            response.append(line)
        return response

    def get_build_props(self):
        """
        Get contents of /system/build.prop as dict.
        Return dictionary like: Property => Value
        """
        build_props = {}
        out = subprocess.check_output([ADB_EXE, "shell",
                                      "cat /system/build.prop"],
                                      universal_newlines=True)
        self.check_output(out)
        for line in out.split('\n'):
            if line == '':
                continue
            prop = line.split('=')
            if not prop[0].startswith('#'):
                build_props[prop[0]] = prop[1]
        return build_props

    def reboot(self, option):
        if option == "system":
            subprocess.call([ADB_EXE, "reboot"])
        elif option in ("recovery", "bootloader"):
            subprocess.call([ADB_EXE, "reboot", option])
        else:
            print("Invalid reboot-option!")

    def check_output(self, out):
        """
        Check if the response of a command is valid.
        """
        if out == "error: device not found":
            sys.exit("Error connecting to device!")

    def __exit__(self, type, value, traceback):
        subprocess.call([ADB_EXE, "kill-server"])


def example():
    print("# Welcome to AndroPy #")
    print("----------------------")
    with ADBInterface() as ai:
        print("Number of devices detected:", len(ai.get_devices()))
        print("Number of your downloaded apps:", len(ai.exec_shell_cmd("ls /data/app")))
        bps = ai.get_build_props()
        print("Your phone's CPU:", bps['ro.device.cpu'])
        print("Your phone's model:", bps['ro.product.manufacturer'], bps['ro.product.device'])


if __name__ == '__main__':
    example()
