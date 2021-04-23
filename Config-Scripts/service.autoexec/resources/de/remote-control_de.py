#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xbmcaddon
import xbmcgui
import subprocess
import time
import os

win = xbmcgui.Window()
width = win.getWidth()
monitor = xbmc.Monitor()
Skipall = False
Cancel = False
y = 100
while not monitor.abortRequested():


	#reset old configuration

	remotefile = open("/storage/.kodi/temp/my_custom_remote","w+")
	remotefile.write ("")
	remotefile.close()

	logfile = open("/storage/IRlog.txt","w+")
	logfile.close()

	process=subprocess.Popen("ir-keytable -p all -v", shell=True)
	time.sleep (1)
	process.terminate()
	remotefile = open("/storage/.kodi/temp/my_custom_remote","a")

		####################Protocol#############################

	win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Tasten Ihrer Fernbedienung mehrere Male.'))
	win.show()
	y += 20

	process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
	pDialog = xbmcgui.DialogProgressBG()
	pDialog.create('Taste hinzufügen', 'Drücken Sie eine Taste Ihrer Fernbedienung mehrere Male')
	logfile = open("/storage/IRlog.txt", "r")
	log = logfile.readline()
	while log == "" and not monitor.abortRequested():
	  log = logfile.readline()
	pDialog.close()
	process.terminate()
	lines = logfile.readlines()
	i = 1
	logfile.close()

	while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile
	  log = lines[i]
	  i+=1

	protocol = (log[log.find('(')+1 : log.find(')')])   #get protocol from log
	if protocol == "necx":
	  protocol = "nec"
	elif protocol == "sony12":
	  protocol = "sony"

	remotefile.write("# table justboom, type: " + protocol + '\n')  #add header to remotefile


	#reset logfile
	logfile = open("/storage/IRlog.txt", "w")
	logfile.write("")
	logfile.close()


	####################KEY_OK#############################
	if Skipall == False:

		ret = xbmcgui.Dialog().select("Konfigurieren der Taste OK", ["Ok", "Taste überspringen", "Alle überspringen"])
		#cID = win.getControl()
		#win.removeControl(cID)
		#win.setLabel('Status')
		#xbmcgui.ControlFadeLabel.reset (ctrl)
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = '---------------------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Taste OK von Ihrer Fernbedienung mehrere Male'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Taste hinzufügen', 'Drücken Sie die Taste OK')
			pDialog.update(9, message='Drücken Sie die Taste OK')
			logfile = open("/storage/IRlog.txt", "r")
			log = logfile.readline()
			while log == "" and not monitor.abortRequested():
			  log = logfile.readline()
			pDialog.close()
			process.terminate()

			lines = logfile.readlines()
			i = 1

			logfile.close()

			while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile

			  log = lines[i]
			  i+=1

			protocol = (log[log.find('(')+1 : log.find(')')])   #get protocol from log
			if protocol == "necx":
			  protocol = "nec"
			elif protocol == "sony12":
			  protocol = "sony"
			code = (log[log.find('= ')+2 : log.find('/n')])     #get scancode from log


			#print (code)
			#print(protocol)

			remotefile.write(code + " KEY_OK" + '\n')                       #add KEY_OK to remotefile


			#reset logfile
			logfile = open("/storage/IRlog.txt", "w")
			logfile.write("")
			logfile.close()


		####################KEY_EXIT#############################
	if Skipall == False:

		ret = xbmcgui.Dialog().select("Konfigurieren der Taste EXIT", ["Ok", "Taste überspringen", "Alles überspringen"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = '---------------------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Taste EXIT von Ihrer Fernbedienung mehrere Male'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Taste hinzufügen', 'Drücken Sie die Taste EXIT')
			pDialog.update(18, message='Drücken Sie die Taste EXIT')
			logfile = open("/storage/IRlog.txt", "r")
			log = logfile.readline()
			while log == "":
			  log = logfile.readline()
			pDialog.close()
			process.terminate()
			#xbmcgui.Dialog().ok(addonname, "Taste erkannt")
			#time.sleep(1)
			lines = logfile.readlines()
			i = 1

			logfile.close()
			while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile

			  log = lines[i]
			  i+=1

			code = (log[log.find('= ')+2 : log.find('/n')])     #get scancode from log

			#print (code)

			remotefile.write(code + " KEY_EXIT" + '\n')                       #add KEY_EXIT to remotefile

			#reset logfile
			logfile = open("/storage/IRlog.txt", "w")
			logfile.write("")
			logfile.close()

	####################KEY_LEFT#############################
	if Skipall == False:

		ret = xbmcgui.Dialog().select("Konfigurieren der Taste LINKS", ["Ok", "Taste überspringen", "Alles überspringen"])
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = '---------------------------------------------------------------------------------------------------------------------'))
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Taste LINKS (<) von Ihrer Fernbedienung mehrere Male'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Taste hinzufügen', 'Drücken Sie die Taste LINKS')
			pDialog.update(27, message='Drücken Sie die Taste LINKS')
			logfile = open("/storage/IRlog.txt", "r")
			log = logfile.readline()
			while log == "":
			  log = logfile.readline()
			pDialog.close()
			process.terminate()
			#xbmcgui.Dialog().ok(addonname, "Taste erkannt")
			#time.sleep(1)
			lines = logfile.readlines()
			i = 1

			logfile.close()
			while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile

			  log = lines[i]
			  i+=1

			code = (log[log.find('= ')+2 : log.find('/n')])     #get scancode from log

			#print (code)

			remotefile.write(code + " KEY_LEFT" + '\n')                       #add KEY_LEFT to remotefile

			#reset logfile
			logfile = open("/storage/IRlog.txt", "w")
			logfile.write("")
			logfile.close()

	####################KEY_RIGHT#############################
	if Skipall == False:

		ret = xbmcgui.Dialog().select("Konfigurieren der Taste RECHTS", ["Ok", "Taste überspringen", "Alles überspringen"])
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = '---------------------------------------------------------------------------------------------------------------------'))
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Taste RECHTS (>) von Ihrer Fernbedienung mehrere Male'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Taste hinzufügen', 'Drücken Sie die Taste RECHTS')
			pDialog.update(36, message='Drücken Sie die Taste RECHTS')
			logfile = open("/storage/IRlog.txt", "r")
			log = logfile.readline()
			while log == "":
			  log = logfile.readline()
			pDialog.close()
			process.terminate()
			#xbmcgui.Dialog().ok(addonname, "Taste erkannt")
			#time.sleep(1)
			lines = logfile.readlines()
			i = 1

			logfile.close()
			while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile

			  log = lines[i]
			  i+=1

			code = (log[log.find('= ')+2 : log.find('/n')])     #get scancode from log

			#print (code)

			remotefile.write(code + " KEY_RIGHT" + '\n')                       #add KEY_RIGHT to remotefile

			#reset logfile
			logfile = open("/storage/IRlog.txt", "w")
			logfile.write("")
			logfile.close()
	####################KEY_UP#############################
	if Skipall == False:
		pDialog.update(45, message='Drücken Sie die Taste OBEN von Ihrer Fernbedienung mehrere Male')
		ret = xbmcgui.Dialog().select("Konfigurieren der Taste OBEN", ["Ok", "Taste überspringen", "Alles überspringen"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = '---------------------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Taste OBEN (^) von Ihrer Fernbedienung mehrere Male'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Taste hinzufügen', 'Drücken Sie die Taste OBEN')
			pDialog.update(45, message='Drücken Sie die Taste OBEN')
			logfile = open("/storage/IRlog.txt", "r")
			log = logfile.readline()
			while log == "":
			  log = logfile.readline()
			pDialog.close()
			process.terminate()
			#xbmcgui.Dialog().ok(addonname, "Taste erkannt")
			#time.sleep(1)
			lines = logfile.readlines()
			i = 1

			logfile.close()
			while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile

			  log = lines[i]
			  i+=1

			code = (log[log.find('= ')+2 : log.find('/n')])     #get scancode from log

			#print (code)

			remotefile.write(code + " KEY_UP" + '\n')                       #add KEY_UP to remotefile

			#reset logfile
			logfile = open("/storage/IRlog.txt", "w")
			logfile.write("")
			logfile.close()

	####################KEY_DOWN#############################
	if Skipall == False:

		ret = xbmcgui.Dialog().select("Konfigurieren der Taste UNTEN", ["Ok", "Taste überspringen", "Alles überspringen"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = '---------------------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Taste UNTEN (v) von Ihrer Fernbedienung mehrere Male'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Taste hinzufügen', 'Drücken Sie die Taste UNTEN')
			pDialog.update(54, message='Drücken Sie die Taste UNTEN')
			logfile = open("/storage/IRlog.txt", "r")
			log = logfile.readline()
			while log == "":
			  log = logfile.readline()
			pDialog.close()
			process.terminate()
			#xbmcgui.Dialog().ok(addonname, "Taste erkannt")
			#time.sleep(1)
			lines = logfile.readlines()
			i = 1

			logfile.close()
			while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile

			  log = lines[i]
			  i+=1

			code = (log[log.find('= ')+2 : log.find('/n')])     #get scancode from log

			print (code)

			remotefile.write(code + " KEY_DOWN" + '\n')                       #add KEY_DOWN to remotefile

			#reset logfile
			logfile = open("/storage/IRlog.txt", "w")
			logfile.write("")
			logfile.close()
		process.terminate()
	####################KEY_VOLUMEDOWN#############################

	if Skipall == False:

		ret = xbmcgui.Dialog().select("Konfigurieren der Taste LEISER", ["Ok", "Taste überspringen", "Alles überspringen"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = '---------------------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Taste LEISER von Ihrer Fernbedienung mehrere Male'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Taste hinzufügen', 'Drücken Sie die Taste LEISER')
			pDialog.update(63, message='Drücken Sie die Taste LEISER')
			logfile = open("/storage/IRlog.txt", "r")
			log = logfile.readline()
			while log == "":
			  log = logfile.readline()
			pDialog.close()
			process.terminate()
			#xbmcgui.Dialog().ok(addonname, "Press Button: Taste erkannt")
			#time.sleep(1)
			lines = logfile.readlines()
			i = 1

			logfile.close()
			while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile

			  log = lines[i]
			  i+=1

			code = (log[log.find('= ')+2 : log.find('/n')])     #get scancode from log

			print (code)

			remotefile.write(code + " KEY_VOLUMEDOWN" + '\n')                       #add KEY_VOLUMEDOWN to remotefile

			#reset logfile
			logfile = open("/storage/IRlog.txt", "w")
			logfile.write("")
			logfile.close()

	####################KEY_VOLUMEUP#############################
	if Skipall == False:

		ret = xbmcgui.Dialog().select("Konfigurieren der Taste LAUTER", ["Ok", "Taste überspringen", "Alles überspringen"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = '---------------------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Taste LAUTER von Ihrer Fernbedienung mehrere Male'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Taste hinzufügen', 'Drücken Sie die Taste LAUTER')
			pDialog.update(72, message='Drücken Sie die Taste LAUTER')
			logfile = open("/storage/IRlog.txt", "r")
			log = logfile.readline()
			while log == "":
			  log = logfile.readline()
			pDialog.close()
			process.terminate()
			#xbmcgui.Dialog().ok(addonname, "Taste erkannt")
			#time.sleep(1)
			lines = logfile.readlines()
			i = 1

			logfile.close()
			while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile

			  log = lines[i]
			  i+=1

			code = (log[log.find('= ')+2 : log.find('/n')])     #get scancode from log

			print (code)

			remotefile.write(code + " KEY_VOLUMEUP" + '\n')                       #add KEY_VOLUMEUP to remotefile

			#reset logfile
			logfile = open("/storage/IRlog.txt", "w")
			logfile.write("")
			logfile.close()

	####################KEY_MUTE#############################
	if Skipall == False:

		ret = xbmcgui.Dialog().select("Konfigurieren der Taste MUTE", ["Ok", "Taste überspringen", "Alles überspringen"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = '---------------------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Taste MUTE von Ihrer Fernbedienung mehrere Male'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Taste hinzufügen', 'Drücken Sie die Taste MUTE')
			pDialog.update(81, message='Drücken Sie die Taste MUTE')
			logfile = open("/storage/IRlog.txt", "r")
			log = logfile.readline()
			while log == "":
			  log = logfile.readline()
			pDialog.close()
			process.terminate()
			#xbmcgui.Dialog().ok(addonname, "Taste erkannt")
			#time.sleep(1)
			lines = logfile.readlines()
			i = 1

			logfile.close()
			while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile

			  log = lines[i]
			  i+=1

			code = (log[log.find('= ')+2 : log.find('/n')])     #get scancode from log

			print (code)

			remotefile.write(code + " KEY_MUTE" + '\n')                       #add KEY_MUTE to remotefile

			#reset logfile
			logfile = open("/storage/IRlog.txt", "w")
			logfile.write("")
			logfile.close()

	####################KEY_PLAYPAUSE#############################
	if Skipall == False:

		ret = xbmcgui.Dialog().select("Konfigurieren der Taste START/STOPP", ["Ok", "Taste überspringen", "Alles überspringen"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = '---------------------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = 'Drücken Sie die Taste START/STOPP von Ihrer Fernbedienung mehrere Male'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Taste hinzufügen', 'Drücken Sie die Taste START/STOPP')
			pDialog.update(90, message='Drücken Sie die Taste START/STOPP')
			logfile = open("/storage/IRlog.txt", "r")
			log = logfile.readline()
			while log == "":
			  log = logfile.readline()
			pDialog.close()
			process.terminate()
			#xbmcgui.Dialog().ok(addonname, "Taste erkannt")
			#time.sleep(1)
			lines = logfile.readlines()
			i = 1

			logfile.close()
			while log.find("scancode") == -1 or log.find("protocol") == -1 or log.find("repeat") != -1 or log.find("toggle") != -1:  #suche nach der richtigen Zeile

			  log = lines[i]
			  i+=1

			code = (log[log.find('= ')+2 : log.find('/n')])     #get scancode from log

			print (code)

			remotefile.write(code + " KEY_PLAYPAUSE" + '\n')                       #add KEY_PLAYPAUSE to remotefile

			#reset logfile
			logfile = open("/storage/IRlog.txt", "w")
			logfile.write("")
			logfile.close()

	#################
	remotefile.close()
	os.system("rm /storage/IRlog.txt")
	if Cancel == False:
		os.system("rm /storage/.config/rc_keymaps/my_custom_remote")
		os.system("cp /storage/.kodi/temp/my_custom_remote /storage/.config/rc_keymaps/my_custom_remote")
		#os.system("rm /storage/.kodi/temp/my_custom_remote")
		conffile = open("/storage/.config/rc_maps.cfg", "w")
		conffile.write("* * my_custom_remote")
		conffile.close()
		xbmcgui.Dialog().ok("Konfiguration der Fernbedienung", "Deine Fernbedienung wurde erfolgreich eingerichtet!")
		os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/de/end_de.py\")'")
	else:
		conffile = open("/storage/.config/rc_maps.cfg", "w")
		conffile.write("")
		conffile.close()

		remotefile = open("/storage/.config/rc_keymaps/my_custom_remote","w")
		remotefile.write ("")
		remotefile.close()
		os.system("rm /storage/.kodi/temp/my_custom_remote")
		xbmcgui.Dialog().ok("Konfiguration der Fernbedienung", "Abgebrochen! Konfiguration wurde unterbrochen!")
		os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/de/end_de.py\")'")






	break
