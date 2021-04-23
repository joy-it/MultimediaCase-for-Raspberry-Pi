#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xbmcaddon
import xbmcgui
import subprocess
import time
import os


monitor = xbmc.Monitor()
language = xbmcgui.Dialog().select("Choose a language",["English", "Deutsch"])
if language == -1:
    os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/starting-program.py\")'")
if language == 0:
    os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/en/start_en.py\")'")
if language == 1:
    os.system("python /storage/.kodi/addons/service.autoexec/resources/de/language-set_de.py")
