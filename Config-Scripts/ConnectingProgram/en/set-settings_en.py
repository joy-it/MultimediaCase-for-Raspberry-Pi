# MultimediaCase for Raspberry Pi - by Joy-IT
# Addon published under MIT-License

import sys
import xbmcaddon
import xbmcgui
import subprocess
import time
import os

os.system("touch /storage/.kodi/temp/temp.txt")
with open("/storage/.kodi/userdata/autoexec.py","r") as log, open("/storage/.kodi/temp/temp.txt","w") as file:
    for line in log:
        if not "kodi-send --action=" in line:
            file.write(line)
os.system("rm /storage/.kodi/userdata/autoexec.py && touch /storage/.kodi/userdata/autoexec.py")
os.system("cp /storage/.kodi/temp/temp.txt /storage/.kodi/userdata/autoexec.py")
os.system("rm /storage/.kodi/temp/temp.txt")
with open("/storage/.kodi/userdata/autoexec.py","a") as log:
    log.write("os.system(\"kodi-send --action='RunScript(\\\"/storage/ConnectingProgram/en/set-settings_en.py\\\")'\")\n")

setRemote = xbmcgui.Dialog().yesno("Configuration","Do you want to set a remote control?")
if setRemote == True:
    os.system("kodi-send --action='RunScript(\"/storage/ConnectingProgram/en/remote-control_en.py\")'")
if setRemote == False:
    os.system("kodi-send --action='RunScript(\"/storage/ConnectingProgram/en/end_en.py\")'")
