#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MultimediaCase for Raspberry Pi - by Joy-IT
# Addon published under MIT-License

import sys
import xbmcaddon
import xbmcgui
import subprocess
import time
import os

with open("/storage/.kodi/userdata/autoexec.py","r") as log, open("/storage/.kodi/temp/temp.txt","w") as file:
    for line in log:
        if not "kodi-send --action=" in line:
            file.write(line)
os.system("rm /storage/.kodi/userdata/autoexec.py && touch /storage/.kodi/userdata/autoexec.py")
os.system("cp /storage/.kodi/temp/temp.txt /storage/.kodi/userdata/autoexec.py")
os.system("rm /storage/.kodi/temp/temp.txt")
with open("/storage/.kodi/userdata/autoexec.py","a") as log:
    log.write("os.system(\"kodi-send --action='RunScript(\\\"/storage/ConnectingProgram/de/end_de.py\\\")'\")\n")

xbmcgui.Dialog().ok("Konfiguration","Sie haben erfolgreich Ihr MultimediaCase eingerichtet.")
xbmcgui.Dialog().textviewer("Konfiguration","Sie können die bereits vorinstallierten Addons dazu nutzen, die nun getätigten Einstellungen abzuändern.\nDer Raspberry Pi wird nun neustarten um die Einstellungen abzuspeichern.")
os.system("touch /storage/.kodi/temp/temp.txt")

with open("/storage/.kodi/userdata/autoexec.py","r") as log, open("/storage/.kodi/temp/temp.txt","w") as file:
    for line in log:
        if not "kodi-send --action=" in line:
            file.write(line)
os.system("rm /storage/.kodi/userdata/autoexec.py && touch /storage/.kodi/userdata/autoexec.py")
os.system("cp /storage/.kodi/temp/temp.txt /storage/.kodi/userdata/autoexec.py")
os.system("rm /storage/.kodi/temp/temp.txt")
with open("/storage/.kodi/userdata/autoexec.py","a") as log:
        log.write("os.system(\"python /storage/ConnectingProgram/delete-everything.py\")\n")
time.sleep(2)
os.system("reboot")
