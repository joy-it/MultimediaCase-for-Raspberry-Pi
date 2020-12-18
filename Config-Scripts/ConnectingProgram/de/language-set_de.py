# MultimediaCase for Raspberry Pi - by Joy-IT
# Addon published under MIT-License

import os
from time import sleep

os.system("touch /storage/.kodi/temp/temp.txt")
with open("/storage/.kodi/userdata/autoexec.py","r") as log, open("/storage/.kodi/temp/temp.txt","w") as file:
    for line in log:
        if not "kodi-send --action=" in line:
            file.write(line)
os.system("rm /storage/.kodi/userdata/autoexec.py && touch /storage/.kodi/userdata/autoexec.py")
os.system("cp /storage/.kodi/temp/temp.txt /storage/.kodi/userdata/autoexec.py")
os.system("rm /storage/.kodi/temp/temp.txt")

os.system("touch /storage/ConnectingProgram/start-defence_de.txt")
os.system("systemctl stop kodi")
os.system("rm /storage/.kodi/userdata/guisettings.xml && touch /storage/.kodi/userdata/guisettings.xml")
os.system("cp /storage/ConnectingProgram/de/german.xml /storage/.kodi/userdata/guisettings.xml")
os.system("systemctl start kodi")
sleep(4)
with open("/storage/.config/autostart.sh","r") as log, open("/storage/.kodi/temp/temp.txt","w") as file:
    for line in log:
        if not "python /storage/ConnectingProgram/kodi-defence.py &" in line:
            file.write(line)
os.system("rm /storage/.config/autostart.sh && touch /storage/.config/autostart.sh")
os.system("cp /storage/.kodi/temp/temp.txt /storage/.config/autostart.sh")
os.system("rm /storage/.kodi/temp/temp.txt")
os.system("kodi-send --action='RunScript(\"/storage/ConnectingProgram/de/start_de.py\")'")
