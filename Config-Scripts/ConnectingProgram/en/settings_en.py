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
    fan = xbmcgui.Dialog().select("Do you want to activate fan control?", ["Activate", "Deactivate","More information"])
    if fan == -1:
        Cancel = True
    if fan == 1:
        xbmcgui.Dialog().ok("Status of fan control","The fan control is deactivated.")
    if fan == 0:
		with open("/storage/.kodi/temp/functions.txt", "a") as log:
			log.write("python /storage/.kodi/addons/script.module.MultimediaCase/lib/fan.py &\n")
		xbmcgui.Dialog().ok("Status of fan control","The fan control is activated.")
		status_Fan = True
    if fan == 2:
        xbmcgui.Dialog().ok("Fan control HELP","This is a program which observes the temperature of the Raspberry Pi. It cools the Pi down to 50C if it reaches a temperature of 60C. This can also be adjusted to your wishes in the corresponding code")
        fanControll()

def learningMode():
    global Cancel
    global status_LearningMode
    if Cancel == False:
        learning_Mode = xbmcgui.Dialog().select("Do you want to set a new PowerOff-Button at your remote control?", ["Yes", "No","More information"])

        if learning_Mode == -1:
            Cancel = True
        if learning_Mode == 1:
            xbmcgui.Dialog().ok("Status of Learning Mode","Skipped setting.")
        if learning_Mode == 0:
            ser = serial.Serial(port='/dev/serial0', baudrate = 38400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

            ser.write(str.encode('\x0D'))
            ser.write(str.encode('X04'))
            ser.write(str.encode('\x0D'))
            time.sleep(.1)
            ser.write(str.encode('000\r'))
            xbmcgui.Dialog().textviewer("Configuration of PowerOff-Button","The Case is now blinking in different colours to mark that it is waiting for an infrared signal. It will light up in white if it receives a signal. You have to press the selected button 3 times to confirm the selection. If you should press another button, the case will light up in red and will wait that you press the same button 3 times again. If the LEDs light in green again, the selection of the PowerOff-Button is made and you can continue with ENTER.")
            xbmcgui.Dialog().ok("Status of Learning Mode","New button is set as PowerOff-Button.")
            status_LearningMode = True
        if learningMode == 2:
            xbmcgui.Dialog().ok("PowerOff-Button HELP", "This is can be a button of a remote control to shutdown your Multimedia Case. It can be any button of a infrared remote control of your choice.")

while not monitor.abortRequested():
    fanControll()
    learningMode()
    if Cancel == False:
        os.system("rm /storage/.config/autostart.sh && touch /storage/.config/autostart.sh")
        os.system("cp /storage/.kodi/temp/functions.txt /storage/.config/autostart.sh")
        os.system("rm /storage/.kodi/temp/functions.txt")
        if status_Fan == False and status_LearningMode == False:
            xbmcgui.Dialog().ok("Settings of MultimediaCase", "You have successfully deactivated fan control. No new power off button was learned.")
        elif status_Fan == True and status_LearningMode == False:
            xbmcgui.Dialog().ok("Settings of MultimediaCase", "You have successfully activated fan control. No new power off button was learned.")
        elif status_Fan == False and status_LearningMode == True:
            xbmcgui.Dialog().ok("Settings of MultimediaCase", "You have successfully deactivated fan control. A new power off button was learned.")
        elif status_Fan == True and status_LearningMode == True:
            xbmcgui.Dialog().ok("Settings of MultimediaCase", "You have successfully activated fan control. A new power off button was learned.")
        os.system("kodi-send --action='RunScript(\"/storage/ConnectingProgram/en/set-settings_en.py\")'")

    else:
        os.system("rm /storage/.kodi/temp/functions.txt")
        xbmcgui.Dialog().ok("Settings of MultimediaCase", "Cancelled! Configuration aborted!")
        os.system("kodi-send --action='RunScript(\"/storage/ConnectingProgram/en/set-settings_en.py\")'")

    break
