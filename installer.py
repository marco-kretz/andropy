#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import os
import sys
import urllib.request as urll
from os.path import expanduser


adb_link = "https://github.com/tehmk/androgola-platform-tools/raw/master/"

class Installer():
    def __init__(self, adb, fastboot):
        self.adb = adb
        self.fastboot = fastboot
        self.arch = platform.architecture()[0]
        self.os = platform.system().lower()
        self.homedir = expanduser("~")

    def execute(self):
        def create_download_url(tool):
            if tool in ("adb", "fastboot"):
                return adb_link + self.os + "/" + tool + self.arch[:2]

        adb_dl = create_download_url("adb")
        fb_dl = create_download_url("fastboot")
        try:
            os.makedirs(self.homedir + "/.andropy/bin", exist_ok=True)
            if self.adb:
                urll.urlretrieve(adb_dl, self.homedir+"/.andropy/bin/adb")
            if self.fastboot:
                urll.urlretrieve(fb_dl, self.homedir+"/.andropy/bin/fastboot")
        except OSError:
            sys.exit("Folder creation failed!")




i = Installer(True, False)
print("ADB:", i.adb)
print("Fastboot:", i.fastboot)
print("Arch:", i.arch)
print("OS:", i.os)
print("Location:", i.homedir)

i.execute()
