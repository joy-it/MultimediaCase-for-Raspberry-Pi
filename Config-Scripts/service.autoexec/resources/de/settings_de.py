#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

def fanControl():
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
        xbmcgui.Dialog().ok("Lüftersteuerung HILFE","Dieses Programm steuert den eingebauten Lüfter im Multimedia Case. Der Lüfter kühlt den Pi bis zu 50C herunter, wenn dieser eine Temperatur von 60C überschritten hat. Dies kann auch im dazugehörigen Code angepasst werden.")
        fanControl()

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

            xbmcgui.Dialog().textviewer("Konfiguration der PowerOff-Taste", "Das Multimedia Case beginnt bunt zu blinken. Nun müssen Sie eine beliebige Taste dreimal betätigen, damit diese als PowerOff-Button gesetzt wird. Wenn ein Signal empfangen wird, leuchtet das Multimedia Case weiß auf. Wenn jedoch eine andere Taste betätigt wird, als die vorherigen, dann leuchtet das Gehäuse rot auf und es muss erneut dreimal eine beliebige Taste betätigt werden. Das Gehäuse wird grün aufleuchten, wenn erfolgreich ein neuer PowerOff-Button gesetzt wurde.\n Sie können mit ENTER fortfahren.")
            status_LearningMode = True
        if learning_Mode == 2:
            xbmcgui.Dialog().ok("PowerOff-Button HILFE", "Mit diesem Programm können Sie eine Taste einer beliebigen Fernbedienung als An- und Austaste des Multimedia Cases konfigurieren. Weitere Tasten zur Steuerung des Systems können im Addon IR Control Configuration konfiguriert werden.")
            learningMode()

while not monitor.abortRequested():
    fanControl()
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
        os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/de/set-settings_de.py\")'")

    else:
        os.system("rm /storage/.kodi/temp/functions.txt")
        xbmcgui.Dialog().ok("Funktionen des MultimediaCases", "Abgebrochen! Konfiguration wurde unterbrochen!")
        os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/de/set-settings_de.py\")'")

    break
