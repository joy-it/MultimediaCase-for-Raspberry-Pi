# MultimediaCase for Raspberry Pi - by Joy-IT
# Addon published under MIT-License

import xbmcaddon
import xbmcgui
import subprocess
import time
import os

win = xbmcgui.Window()
width = win.getWidth()
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
_localize_ = addon.getLocalizedString
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

	ret = xbmcgui.Dialog().select(_localize_(32001), [_localize_(32002), _localize_(32003)])
	win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = _localize_(32004)))
	win.show()
	y += 20
	if ret == 1 or ret == -1:
		Skipall = True
	if ret == -1:
		Cancel = True
	if ret == 0:
		process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
		pDialog = xbmcgui.DialogProgressBG()
		pDialog.create(_localize_(32005), _localize_(32006))
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

		ret = xbmcgui.Dialog().select(_localize_(32007), [_localize_(32002), _localize_(32008), _localize_(32009)])
		#cID = win.getControl()
		#win.removeControl(cID)
		#win.setLabel('Status')
		#xbmcgui.ControlFadeLabel.reset (ctrl)
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = _localize_(32010)))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = _localize_(32011)))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create(_localize_(32005), _localize_(32012))
			pDialog.update(9, message=_localize_(32012))
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

		ret = xbmcgui.Dialog().select(_localize_(32013), [_localize_(32002), _localize_(32008), _localize_(32009)])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = _localize_(32010)))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = _localize_(32014)))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create(_localize_(32005), _localize_(32015))
			pDialog.update(18, message=_localize_(32015))
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

		ret = xbmcgui.Dialog().select(_localize_(32016), [_localize_(32002), _localize_(32008), _localize_(32009)])
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = _localize_(32010)))
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = _localize_(32017)))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create(_localize_(32005),_localize_(32018))
			pDialog.update(27, message=_localize_(32018))
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

		ret = xbmcgui.Dialog().select(_localize_(32019), [_localize_(32002), _localize_(32008), _localize_(32009)])
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = _localize_(32010)))
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = _localize_(32020)))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create(_localize_(32005), _localize_(32021))
			pDialog.update(36, message=_localize_(32021))
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
		pDialog.update(45, message=_localize_(32022))
		ret = xbmcgui.Dialog().select(_localize_(32023), [_localize_(32002), _localize_(32008), _localize_(32009)])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = _localize_(32010)))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = _localize_(32024)))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create(_localize_(32005), _localize_(32022))
			pDialog.update(45, message=_localize_(32022))
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

		ret = xbmcgui.Dialog().select(_localize_(32025), [_localize_(32002), _localize_(32008), _localize_(32009)])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = _localize_(32010)))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = _localize_(32026)))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create(_localize_(32005), _localize_(32027))
			pDialog.update(54, message=_localize_(32027))
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

		ret = xbmcgui.Dialog().select(_localize_(32028), [_localize_(32002), _localize_(32008), _localize_(32009)])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = _localize_(32010)))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label =_localize_(32029)))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create(_localize_(32005), _localize_(32030))
			pDialog.update(63, message=_localize_(32030))
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

		ret = xbmcgui.Dialog().select(_localize_(32031), [_localize_(32002), _localize_(32008), _localize_(32009)])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = _localize_(32010)))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = _localize_(32032)))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create(_localize_(32005), _localize_(32033))
			pDialog.update(72, message=_localize_(32033))
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

		ret = xbmcgui.Dialog().select(_localize_(32034), [_localize_(32002), _localize_(32008), _localize_(32009)])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = _localize_(32010)))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = _localize_(32035)))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create(_localize_(32005), _localize_(32036))
			pDialog.update(81, message=_localize_(32036))
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

		ret = xbmcgui.Dialog().select(_localize_(32037), [_localize_(32002), _localize_(32008), _localize_(32009)])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 750 ,  height = 25 ,  label = _localize_(32010)))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 750 ,  height = 25 ,  label = _localize_(32038)))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create(_localize_(32005), _localize_(32039))
			pDialog.update(90, message=_localize_(32039))
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
		xbmcgui.Dialog().ok(addonname,_localize_(32040))
		os.system ("reboot")
	else:
		conffile = open("/storage/.config/rc_maps.cfg", "w")
		conffile.write("")
		conffile.close()

		remotefile = open("/storage/.config/rc_keymaps/my_custom_remote","w")
		remotefile.write ("")
		remotefile.close()
		os.system("rm /storage/.kodi/temp/my_custom_remote")
		xbmcgui.Dialog().ok(addonname,_localize_(32041))






	break
