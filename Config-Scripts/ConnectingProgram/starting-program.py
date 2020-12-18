#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MultimediaCase for Raspberry Pi - by Joy-IT
# Addon published under MIT-License

import sys
import xbmcaddon
import xbmcgui
import subprocess
import time
import os


monitor = xbmc.Monitor()
language = xbmcgui.Dialog().select("Choose a language",["English", "Deutsch"])
if language == -1:
    os.system("kodi-send --action='RunScript(\"/storage/ConnectingProgram/starting-program.py\")'")
if language == 0:
    os.system("kodi-send --action='RunScript(\"/storage/ConnectingProgram/en/start_en.py\")'")
if language == 1:
    os.system("python /storage/ConnectingProgram/de/language-set_de.py")
