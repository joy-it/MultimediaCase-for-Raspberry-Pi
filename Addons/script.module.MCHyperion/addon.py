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
_localize_ = addon.getLocalizedString
addonname   = addon.getAddonInfo('name')
monitor = xbmc.Monitor()
Cancel = False
loop = False
boardMode = False
ser = serial.Serial(port='/dev/serial0', baudrate = 38400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
os.system("touch /storage/.config/autostart.sh")
os.system("rm /storage/.kodi/temp/led.txt && touch /storage/.kodi/temp/led.txt")
flags = ["/storage/hyperion/bin/hyperion-remote","systemctl start hyperion.service"]
with open("/storage/.config/autostart.sh","r") as log, open("/storage/.kodi/temp/led.txt","w") as file:
    for line in log:
        if not any(flag in line for flag in flags):
            file.write(line)

def selectingMode():
    global Cancel
    modeSelection = xbmcgui.Dialog().select(_localize_(32001),[_localize_(32002),_localize_(32003),_localize_(32004),_localize_(32005),_localize_(32006),_localize_(32007),_localize_(32008),_localize_(32009),_localize_(32010)])
    if modeSelection == -1:
        Cancel = True
        mode = ''
    elif modeSelection == 0:
        mode ='-c'
    elif modeSelection == 1:
        mode = '-e "Plasma"'
    elif modeSelection == 2:
        mode = '-e "Candle"'
    elif modeSelection == 3:
        mode ='-e "Rainbow mood"'
    elif modeSelection == 4:
        mode = '-e "Rainbow swirl"'
    elif modeSelection == 5:
        mode = '-e "Breath"'
    elif modeSelection == 6:
        mode = '-e "Police Lights Single"'
    elif modeSelection == 7:
        mode = '-e "X-Mas"'
    elif modeSelection == 8:
        mode = '-e "Color traces"'
    else:
        mode = ''
    return mode

def selectingColour(mode):
    global Cancel
    if mode == '-c':
        colourSelection = xbmcgui.Dialog().select(_localize_(32011),[_localize_(32012),_localize_(32013),_localize_(32014),_localize_(32015),_localize_(32016),_localize_(32017),_localize_(32018),_localize_(32019), _localize_(32020),_localize_(32021),_localize_(32022),_localize_(32023), _localize_(32024)])
        if colourSelection == -1:
            Cancel = True
            colour = ''
        elif colourSelection == 0:
            colour = ' white'
            return colour
        elif colourSelection == 1:
            colour = ' FF0000'
        elif colourSelection == 2:
            colour = ' FFFF00'
        elif colourSelection == 3:
            colour = ' FF00FF'
        elif colourSelection == 4:
            colour = ' FF8C00'
        elif colourSelection == 5:
            colour = ' 0000FF'
        elif colourSelection == 6:
            colour = ' 00FF00'
        elif colourSelection == 7:
            colour = ' B23AEE'
        elif colourSelection == 8:
            colour = ' 00868B'
        elif colourSelection == 9:
            colour = ' AB82FF'
        elif colourSelection == 10:
            colour = ' 00FFFF'
        elif colourSelection == 11:
            colour = ' CAFF70'
        elif colourSelection == 12:
            colour = ' FA8072'
    else:
        colour = ''
    return colour

def brightnessRepeat(mode, command):
    global Cancel
    brightnessSettings = xbmcgui.Dialog().select(_localize_(32025),["25%","50%","75%","100%"])
    if brightnessSettings == -1:
        Cancel = True
    elif brightnessSettings == 0:
        bright = '25'
    elif brightnessSettings == 1:
        bright = '50'
    elif brightnessSettings == 2:
        bright = '75'
    elif brightnessSettings == 3:
        bright = '100'

    if Cancel == False:
        commandOfBrightness = "/storage/hyperion/bin/hyperion-remote --brightness %s" % (bright)
        os.system(commandOfBrightness)
        xbmcgui.Dialog().ok(addonname, _localize_(32026))
        selectingBrightness = xbmcgui.Dialog().yesno(addonname,_localize_(32027))
        if selectingBrightness == False:
            os.system("rm /storage/.config/autostart.sh && touch /storage/.config/autostart.sh")
            os.system("cp /storage/.kodi/temp/led.txt /storage/.config/autostart.sh")
            with open("/storage/.config/autostart.sh", "a") as log:
                log.write("systemctl start hyperion.service\n")
                log.write(commandOfBrightness + " && " + command + "\n")
            os.system("rm /storage/.kodi/temp/led.txt")
            xbmcgui.Dialog().ok(addonname, _localize_(32028))
            os.system ("reboot")
        if selectingBrightness == True:
            brightnessRepeat(mode, command)
    else:
        xbmcgui.Dialog().ok(addonname, _localize_(32029))
        os.system("rm /storage/.kodi/temp/led.txt")
        os.system("reboot")

def start():
    global Cancel
    global loop
    mode = selectingMode()
    if Cancel == False:
        colour = selectingColour(mode)
    if Cancel == False:
        command = "/storage/hyperion/bin/hyperion-remote %s%s" % (mode, colour)
        os.system("systemctl start hyperion.service")
        os.system("/storage/hyperion/bin/hyperion-remote --brightness 100 && " + command)
        xbmcgui.Dialog().ok(addonname, _localize_(32030))
        repeat = xbmcgui.Dialog().yesno(addonname,_localize_(32031))
        if repeat == False:
            shortcut = xbmcgui.Dialog().yesno(addonname, _localize_(32032))
            if shortcut == False:
                os.system("rm /storage/.config/autostart.sh && touch /storage/.config/autostart.sh")
                os.system("cp /storage/.kodi/temp/led.txt /storage/.config/autostart.sh")
                with open("/storage/.config/autostart.sh", "a") as log:
                    log.write("systemctl start hyperion.service\n")
                    log.write(command + "\n")
                os.system("rm /storage/.kodi/temp/led.txt")
                xbmcgui.Dialog().ok(addonname, _localize_(32028))
                os.system ("reboot")
            if shortcut == True:
                brightnessRepeat(mode, command)
        if repeat == True:
            loop = True
            start()
    else:
        if loop == False:
            xbmcgui.Dialog().ok(addonname,_localize_(32033))
            os.system("rm /storage/.kodi/temp/led.txt")
        else:
            xbmcgui.Dialog().ok(addonname, _localize_(32029))
            os.system("rm /storage/.kodi/temp/led.txt")
            os.system("reboot")

def startpanel():
    global ser
    global time
    global boardMode
    while not monitor.abortRequested():
        beginn = xbmcgui.Dialog().select(_localize_(32034), [_localize_(32035), _localize_(32036),_localize_(32037),_localize_(32038)])
        if beginn == -1:
            if boardMode == True:
                xbmcgui.Dialog().ok(addonname,_localize_(32051))
                os.system("rm /storage/.kodi/temp/led.txt")
            else:
                xbmcgui.Dialog().ok(addonname,_localize_(32033))
                os.system("rm /storage/.kodi/temp/led.txt")
        if beginn == 1:
            if boardMode == True:
                xbmcgui.Dialog().ok(addonname,_localize_(32051))
                os.system("rm /storage/.kodi/temp/led.txt")
            else:
                xbmcgui.Dialog().ok(addonname,_localize_(32033))
                os.system("rm /storage/.kodi/temp/led.txt")
        if beginn == 2:
            boardMode = True
            mode = xbmcgui.Dialog().select(_localize_(32037), [_localize_(32045), _localize_(32046),_localize_(32047)])
            if mode == -1:
                boardMode = False
                startpanel()
            if mode == 0:
                ser.write(str.encode('\x0D'))
                ser.write(str.encode('LM0'))    # Mode 0
                ser.write(str.encode('\x0D'))

                time.sleep(.1)
                #ser.write(str.encode('000\r')
                time.sleep(.1)
                xbmcgui.Dialog().ok(addonname,_localize_(32048))
                startpanel()

            if mode == 1:
                ser.write(str.encode('\x0D'))
                ser.write(str.encode('LM1'))    # Mode 1
                ser.write(str.encode('\x0D'))

                time.sleep(.1)
                #ser.write(str.encode('000\r')
                xbmcgui.Dialog().ok(addonname,_localize_(32049))
                startpanel()

            if mode == 2:
                ser.write(str.encode('\x0D'))
                ser.write(str.encode('LM2'))    # Mode 2
                ser.write(str.encode('\x0D'))

                time.sleep(.1)
                #ser.write(str.encode('000\r')
                xbmcgui.Dialog().ok(addonname,_localize_(32050))
                startpanel()

        if beginn == 3:
            os.system("systemctl stop hyperion.service")
            xbmcgui.Dialog().ok(addonname,_localize_(32041))
            os.system("rm /storage/.config/autostart.sh && touch /storage/.config/autostart.sh")
            os.system("cp /storage/.kodi/temp/led.txt /storage/.config/autostart.sh")
            os.system("rm /storage/.kodi/temp/led.txt")
            xbmcgui.Dialog().ok(addonname, _localize_(32044))
            os.system ("reboot")
        if beginn == 0:
            start()
        break

startpanel()
