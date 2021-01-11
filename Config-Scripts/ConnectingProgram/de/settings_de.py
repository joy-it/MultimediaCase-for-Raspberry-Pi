#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

monitor = xbmc.Monitor()
Cancel = False
status_Fan = False
status_LearningMode = False

os.system("rm /storage/.kodi/temp/functions.txt && touch /storage/.kodi/temp/functions.txt")
flags = ["python /storage/.kodi/addons/script.module.MultimediaCase/lib/fan.py &\n"]
with open("/storage/.config/autostart.sh","r") as log, open("/storage/.kodi/temp/functions.txt","w") as file:
    for line in log:
        if not any(flag in line for flag in flags):
            file.write(line)
os.system("touch /storage/.kodi/temp/temp.txt")

def fanControll():
    global Cancel
    global status_Fan
    fan = xbmcgui.Dialog().select("Möchten Sie die Lüftersteuerung aktivieren?", ["Aktivieren", "Deaktivieren", "Mehr Informationen"])
    if fan == -1:
        Cancel = True
    if fan == 1:
        xbmcgui.Dialog().ok("Status der Lüftersteuerung","Die Lüftersteuerung ist deaktiviert.")
    if fan == 0:
		with open("/storage/.kodi/temp/functions.txt", "a") as log:
			log.write("python /storage/.kodi/addons/script.module.MultimediaCase/lib/fan.py &\n")
		xbmcgui.Dialog().ok("Status der Lüftersteuerung","Die Lüftersteuerung ist aktiviert.")
		status_Fan = True
    if fan == 2:
        xbmcgui.Dialog().ok("Lüftersteuerung HILFE","Dieses Programm nimmt die Temperatur Ihres Raspberry Pis wahr. Es kühlt den Pi bis zu 50C herunter, wenn dieser eine Temperatur von 60C überschritten hat. Dies kann auch im dazugehörigen Code angepasst werden.")
        fanControll()

def learningMode():
    global status_LearningMode
    global Cancel
    if Cancel == False:
        learning_Mode = xbmcgui.Dialog().select("Möchten Sie eine neue PowerOff-Taste einrichten?", ["Ja", "Nein","Mehr Informationen"])
        if learning_Mode == -1:
            Cancel = True
        if learning_Mode == 1:
            xbmcgui.Dialog().ok("Status des Learning Modes","Einstellung übersprungen.")
        if learning_Mode == 0:
            ser = serial.Serial(port='/dev/serial0', baudrate = 38400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

            ser.write(str.encode('\x0D'))
            ser.write(str.encode('X04'))
            ser.write(str.encode('\x0D'))
            time.sleep(.1)
            ser.write(str.encode('000\r'))
            xbmcgui.Dialog().textviewer("Konfiguration der PowerOff-Taste", "Das Gehäuse blinkt nun in verschiedenen Farben, um zu kennzeichnen, dass das Gehäuse auf das Infrarot-Signal Ihrer Fernbedienung wartet. Das Gehäuse leuchtet weiß auf, wenn es ein Signal empfängt. Sie müssen sich eine Taste auswählen, welche Sie dreimal hintereinander betätigen um Ihre Auswahl zu bestätigen. Wenn Sie einen anderen Knopf drücken sollten, als Sie zuvor betätigt haben, wird das Gehäuse rot aufleuchten und Sie müssen erneut dreimal die selbe Taste betätigen. Wenn das Gehäuse grün aufleuchtet, ist der PowerOff-Button gesetzt und Sie können weiter fortfahren in dem Sie auf ENTER drücken.")
            xbmcgui.Dialog().ok("Status des Learning Modes","Neue Taste als PowerOff-Taste gesetzt.")
            status_LearningMode = True
        if learning_Mode == 2:
            xbmcgui.Dialog().ok("PowerOff-Button HILFE", "Das ist eine Taste auf einer Fernbedienung um das Multimedia Case herunterzufahren. Dies kann eine beliebige Taste auf der Fernbedienung Ihrer Wahl sein.")
            learningMode()

while not monitor.abortRequested():
    fanControll()
    learningMode()
    if Cancel == False:
        if status_Fan == False and status_LearningMode == False:
            xbmcgui.Dialog().ok("Funktionen des MultimediaCases", "Sie haben erfolgreich die Lüftersteuerung deaktiviert. Keine neue PowerOff-Taste wurde gesetzt.")
        elif status_Fan == True and status_LearningMode == False:
            xbmcgui.Dialog().ok("Funktionen des MultimediaCases", "Sie haben erfolgreich die Lüftersteuerung aktiviert. Keine neue PowerOff-Taste wurde gesetzt.")
        elif status_Fan == False and status_LearningMode == True:
            xbmcgui.Dialog().ok("Funktionen des MultimediaCases", "Sie haben erfolgreich die Lüftersteuerung deaktiviert. Eine neue PowerOff-Taste wurde gesetzt.")
        elif status_Fan == True and status_LearningMode == True:
            xbmcgui.Dialog().ok("Funktionen des MultimediaCases", "Sie haben erfolgreich die Lüftersteuerung aktiviert. Eine neue PowerOff-Taste wurde gesetzt.")
        os.system("rm /storage/.config/autostart.sh && touch /storage/.config/autostart.sh")
        os.system("cp /storage/.kodi/temp/functions.txt /storage/.config/autostart.sh")
        os.system("rm /storage/.kodi/temp/functions.txt")
        os.system("kodi-send --action='RunScript(\"/storage/ConnectingProgram/de/set-settings_de.py\")'")

    else:
        os.system("rm /storage/.kodi/temp/functions.txt")
        xbmcgui.Dialog().ok("Funktionen des MultimediaCases", "Abgebrochen! Konfiguration wurde unterbrochen!")
        os.system("kodi-send --action='RunScript(\"/storage/ConnectingProgram/de/set-settings_de.py\")'")

    break
