# MultimediaCase for Raspberry Pi - by Joy-IT
# Addon published under MIT-License

import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')
sys.path.append('/storage/.kodi/addons/script.module.pyserial/lib')
import xbmcaddon
import xbmcgui
import subprocess
import time
import os
import serial

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
_localize_ = addon.getLocalizedString
monitor = xbmc.Monitor()
Cancel = False
status_Fan = False
status_LearningMode = False


os.system("touch /storage/.config/autostart.sh")
os.system("rm /storage/.kodi/temp/functions.txt && touch /storage/.kodi/temp/functions.txt")
flags = ["python /storage/.kodi/addons/script.module.MultimediaCase/lib/fan.py &\n", "python /storage/.kodi/addons/script.module.MultimediaCase/lib/shutdown-function.py &"]
with open("/storage/.config/autostart.sh","r") as log, open("/storage/.kodi/temp/functions.txt","w") as file:
    for line in log:
        if not any(flag in line for flag in flags):
            file.write(line)
with open("/storage/.kodi/temp/functions.txt", "a") as log:
    log.write("python /storage/.kodi/addons/script.module.MultimediaCase/lib/shutdown-function.py &\n")

def fanControll():
    global status_Fan
    global Cancel
    fan = xbmcgui.Dialog().select(_localize_(32001), [_localize_(32002),_localize_(32003),_localize_(32021)])
    if fan == -1:
        Cancel = True
    if fan == 1:
        xbmcgui.Dialog().ok(_localize_(32004),_localize_(32005))
    if fan == 0:
        with open("/storage/.kodi/temp/functions.txt", "a") as log:
            log.write("python /storage/.kodi/addons/script.module.MultimediaCase/lib/fan.py &\n")
        xbmcgui.Dialog().ok(_localize_(32004),_localize_(32006))
        status_Fan = True
    if fan == 2:
        xbmcgui.Dialog().ok(_localize_(32022),_localize_(32023))
        fanControll()

def learningMode():
    global status_LearningMode
    global Cancel
    if Cancel == False:
        learning_Mode = xbmcgui.Dialog().select(_localize_(32007), [_localize_(32008),_localize_(32009),_localize_(32021)])
        if learning_Mode == -1:
            Cancel = True
        if learning_Mode == 1:
            xbmcgui.Dialog().ok(_localize_(32010),_localize_(32011))
        if learning_Mode == 0:
            ser = serial.Serial(port='/dev/serial0', baudrate = 38400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

            ser.write(str.encode('\x0D'))
            ser.write(str.encode('X04'))
            ser.write(str.encode('\x0D'))
            
            xbmcgui.Dialog().textviewer(_localize_(32012),_localize_(32013))
            xbmcgui.Dialog().ok(_localize_(32010),_localize_(32014))
            status_LearningMode = True
        if learning_Mode == 2:
            xbmcgui.Dialog().ok(_localize_(32024),_localize_(32025))
            learningMode()

while not monitor.abortRequested():
    fanControll()
    learningMode()
    if Cancel == False:
        os.system("rm /storage/.config/autostart.sh && touch /storage/.config/autostart.sh")
        os.system("cp /storage/.kodi/temp/functions.txt /storage/.config/autostart.sh")
        os.system("rm /storage/.kodi/temp/functions.txt")
        if status_Fan == False and status_LearningMode == False:
            xbmcgui.Dialog().ok(addonname, _localize_(32015))
        elif status_Fan == True and status_LearningMode == False:
            xbmcgui.Dialog().ok(addonname, _localize_(32016))
        elif status_Fan == False and status_LearningMode == True:
            xbmcgui.Dialog().ok(addonname, _localize_(32017))
        elif status_Fan == True and status_LearningMode == True:
            xbmcgui.Dialog().ok(addonname, _localize_(32018))
        xbmcgui.Dialog().ok(addonname, _localize_(32019))
        os.system ("reboot")

    else:
        os.system("rm /storage/.kodi/temp/functions.txt")
        xbmcgui.Dialog().ok(addonname, _localize_(32020))

    break
