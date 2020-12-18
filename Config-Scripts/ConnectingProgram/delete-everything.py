# MultimediaCase for Raspberry Pi - by Joy-IT
# Addon published under MIT-License

import os
os.system("rm /storage/.kodi/userdata/autoexec.py")
os.system("rm /storage/IRlog.txt")
os.system("rm -r /storage/ConnectingProgram")
os.system("rm /storage/.kodi/temp/kodi.log && rm /storage/.kodi/temp/kodi.old.log")
