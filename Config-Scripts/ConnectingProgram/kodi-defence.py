# MultimediaCase for Raspberry Pi - by Joy-IT
# Addon published under MIT-License

import os
import time

while True:
    if os.path.exists("/storage/ConnectingProgram/start-defence_de.txt") == True:
        time.sleep(2)
        os.system("python /storage/ConnectingProgram/de/language-set_de.py")
        break
