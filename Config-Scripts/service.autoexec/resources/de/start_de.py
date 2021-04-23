#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xbmcaddon
import xbmcgui
import subprocess
import time
import os

with open("/storage/.config/autostart.sh","r") as log, open("/storage/.kodi/temp/temp.txt","w") as file:
    for line in log:
        if not "python /storage/.kodi/addons/service.autoexec/resources/kodi-defence.py &" in line:
            file.write(line)
os.system("rm /storage/.config/autostart.sh && touch /storage/.config/autostart.sh")
os.system("cp /storage/.kodi/temp/temp.txt /storage/.config/autostart.sh")
os.system("rm /storage/.kodi/temp/temp.txt")

os.system("touch /storage/.kodi/temp/temp.txt")
with open("/storage/.kodi/addons/service.autoexec/autoexec.py","r") as log, open("/storage/.kodi/temp/temp.txt","w") as file:
    for line in log:
        if not "kodi-send --action=" in line:
            file.write(line)
os.system("rm /storage/.kodi/addons/service.autoexec/autoexec.py && touch /storage/.kodi/addons/service.autoexec/autoexec.py")
os.system("cp /storage/.kodi/temp/temp.txt /storage/.kodi/addons/service.autoexec/autoexec.py")
os.system("rm /storage/.kodi/temp/temp.txt")

with open("/storage/.kodi/addons/service.autoexec/autoexec.py","a") as log:
    log.write("os.system(\"kodi-send --action='RunScript(\\\"/storage/.kodi/addons/service.autoexec/resources/de/start_de.py\\\")'\")\n")

setSettings = xbmcgui.Dialog().yesno("Konfiguration","Möchten Sie die Funktionen des Multimedia Cases einrichten?")
if setSettings == True:
    os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/de/settings_de.py\")'")
if setSettings == False:
    os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/de/set-settings_de.py\")'")
