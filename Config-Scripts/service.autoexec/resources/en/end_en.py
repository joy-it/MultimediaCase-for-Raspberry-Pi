import sys
import xbmcaddon
import xbmcgui
import subprocess
import time
import os

with open("/storage/.kodi/addons/service.autoexec/autoexec.py","r") as log, open("/storage/.kodi/temp/temp.txt","w") as file:
    for line in log:
        if not "kodi-send --action=" in line:
            file.write(line)
os.system("rm /storage/.kodi/addons/service.autoexec/autoexec.py && touch /storage/.kodi/addons/service.autoexec/autoexec.py")
os.system("cp /storage/.kodi/temp/temp.txt /storage/.kodi/addons/service.autoexec/autoexec.py")
os.system("rm /storage/.kodi/temp/temp.txt")
with open("/storage/.kodi/addons/service.autoexec/autoexec.py","a") as log:
    log.write("os.system(\"kodi-send --action='RunScript(\\\"/storage/.kodi/addons/service.autoexec/resources/en/end_en.py\\\")'\")\n")

xbmcgui.Dialog().ok("Configuration","You have successfully set your Multimedia Case.")
xbmcgui.Dialog().textviewer("Configuration","You can use the preinstalled addons to readjust the previous settings.\n The Raspberry Pi will now restart to save your settings.")

with open("/storage/.kodi/addons/service.autoexec/autoexec.py","r") as log, open("/storage/.kodi/temp/temp.txt","w") as file:
    for line in log:
        if not "kodi-send --action=" in line:
            file.write(line)
os.system("rm /storage/.kodi/addons/service.autoexec/autoexec.py && touch /storage/.kodi/addons/service.autoexec/autoexec.py")
os.system("cp /storage/.kodi/temp/temp.txt /storage/.kodi/addons/service.autoexec/autoexec.py")
os.system("rm /storage/.kodi/temp/temp.txt")
with open("/storage/.kodi/addons/service.autoexec/autoexec.py","a") as log:
        log.write("os.system(\"python /storage/.kodi/addons/service.autoexec/resources/delete-everything.py\")\n")
time.sleep(2)
os.system("reboot")
