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
        xbmcgui.Dialog().ok("Fan control HELP","This program controls the built-in fan in the Multimedia Case. The fan cools the Pi down to 50C when it has exceeded a temperature of 60C. This can also be adjusted in the corresponding code.")
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

            xbmcgui.Dialog().textviewer("Configuration of PowerOff-Button","When a new key is learned, the Multimedia Case starts flashing colourfully. Now, you have to press any key three times to set it as the PowerOff-Button. When a signal is received, the Multimedia Case lights up white. However, if any key is pressed other than the previous one, the case will light up red and you have to press any key three times again. The case will light green if a new PowerOff-Button has been successfully set.\nYou can continue with ENTER.")
            xbmcgui.Dialog().ok("Status of Learning Mode","New button is set as PowerOff-Button.")
            status_LearningMode = True
        if learningMode == 2:
            xbmcgui.Dialog().ok("PowerOff-Button HELP", "With this program you can set a button of any remote control as on/off button of the Multimedia Case. More buttons to control the system can be configured in the IR Control Configuration addon.")

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
        os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/en/set-settings_en.py\")'")

    else:
        os.system("rm /storage/.kodi/temp/functions.txt")
        xbmcgui.Dialog().ok("Settings of MultimediaCase", "Cancelled! Configuration aborted!")
        os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/en/set-settings_en.py\")'")

    break
