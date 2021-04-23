import os
import time

while True:
    if os.path.exists("/storage/.kodi/addons/service.autoexec/resources/start-defence_de.txt") == True:
        time.sleep(10)
        os.system("rm /storage/.kodi/userdata/guisettings.xml && touch /storage/.kodi/userdata/guisettings.xml")
        os.system("cp /storage/.kodi/addons/service.autoexec/resources/de/german.xml /storage/.kodi/userdata/guisettings.xml")
        os.system("systemctl start kodi")
        time.sleep(2)
        os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/de/start_de.py\")'")
        break
