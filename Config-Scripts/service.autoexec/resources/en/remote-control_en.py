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

	win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press any button on your remote control several times'))
	win.show()
	y += 20
	process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
	pDialog = xbmcgui.DialogProgressBG()
	pDialog.create('Add Key', 'Press any Button on your IR-Remote several times')
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

		ret = xbmcgui.Dialog().select("Configure Button OK", ["Ok", "Skip this Key", "Skip all"])
		#cID = win.getControl()
		#win.removeControl(cID)
		#win.setLabel('Status')
		#xbmcgui.ControlFadeLabel.reset (ctrl)
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 700 ,  height = 25 ,  label = '-------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press button OK on your remote control several times'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Add Key', 'Press Button: OK on your IR-Remote several times')
			pDialog.update(9, message='Press Button: OK on your IR-Remote several times')
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

		ret = xbmcgui.Dialog().select("Configure Button EXIT", ["Ok", "Skip this Key", "Skip all"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 700 ,  height = 25 ,  label = '-------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press button EXIT on your remote control several times'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Add Key', 'Press Button: EXIT on your IR-Remote several times')
			pDialog.update(18, message='Press Button: EXIT on your IR-Remote several times')
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

		ret = xbmcgui.Dialog().select("Configure Button LEFT", ["Ok", "Skip this Key", "Skip all"])
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 700 ,  height = 25 ,  label = '-------------------------------------------------------------------------------------------------------'))
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press button LEFT (<) on your remote control several times'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Add Key', 'Press Button: LEFT on your IR-Remote several times')
			pDialog.update(27, message='Press Button: LEFT on your IR-Remote several times')
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

		ret = xbmcgui.Dialog().select("Configure Button RIGHT", ["Ok", "Skip this Key", "Skip all"])
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 700 ,  height = 25 ,  label = '-------------------------------------------------------------------------------------------------------'))
		ctrl = win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press button RIGHT (>) on your remote control several times'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Add Key', 'Press Button: RIGHT on your IR-Remote several times')
			pDialog.update(36, message='Press Button: RIGHT on your IR-Remote several times')
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
		pDialog.update(45, message='Press Button: UP on your IR-Remote several times')
		ret = xbmcgui.Dialog().select("Configure Button UP", ["Ok", "Skip this Key", "Skip all"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 700 ,  height = 25 ,  label = '-------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press button UP (^) on your remote control several times'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Add Key', 'Press Button: UP on your IR-Remote several times')
			pDialog.update(45, message='Press Button: UP on your IR-Remote several times')
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

		ret = xbmcgui.Dialog().select("Configure Button DOWN", ["Ok", "Skip this Key", "Skip all"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 700 ,  height = 25 ,  label = '-------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press button DOWN (v) on your remote control several times'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Add Key', 'Press Button: DOWN on your IR-Remote several times')
			pDialog.update(54, message='Press Button: DOWN on your IR-Remote several times')
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

		ret = xbmcgui.Dialog().select("Configure Button VOLUMEDOWN", ["Ok", "Skip this Key", "Skip all"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 700 ,  height = 25 ,  label = '-------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press button VOLUMEDOWN on your remote control several times'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Add Key', 'Press Button: VOLUMEDOWN on your IR-Remote several times')
			pDialog.update(63, message='Press Button: VOLUMEDOWN on your IR-Remote several times')
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

		ret = xbmcgui.Dialog().select("Configure Button VOLUMEUP", ["Ok", "Skip this Key", "Skip all"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 700 ,  height = 25 ,  label = '-------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press button VOLUMEUP on your remote control several times'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Add Key', 'Press Button: VOLUMEUP on your IR-Remote several times')
			pDialog.update(72, message='Press Button: VOLUMEUP on your IR-Remote several times')
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

		ret = xbmcgui.Dialog().select("Configure Button MUTE", ["Ok", "Skip this Key", "Skip all"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 700 ,  height = 25 ,  label = '-------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press button MUTE on your remote control several times'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Add Key', 'Press Button: MUTE on your IR-Remote several times')
			pDialog.update(81, message='Press Button: MUTE on your IR-Remote several times')
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

		ret = xbmcgui.Dialog().select("Configure Button PLAY/PAUSE", ["Ok", "Skip this Key", "Skip all"])
		win.addControl ( xbmcgui.ControlLabel ( x = 187 ,  y = y - 20 , width = 700 ,  height = 25 ,  label = '-------------------------------------------------------------------------------------------------------'))
		win.addControl ( xbmcgui.ControlLabel ( x = 190 ,  y = y , width = 700 ,  height = 25 ,  label = 'Press button PLAY/PAUSE on your remote control several times'))
		win.show()
		y += 20
		if ret == 2 or ret == -1:
			Skipall = True
		if ret == -1:
			Cancel = True
		if ret == 0:
			process=subprocess.Popen("ir-keytable -t >> /storage/IRlog.txt", shell=True)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Add Key', 'Press Button: PLAY/PAUSE on your IR-Remote several times')
			pDialog.update(90, message='Press Button: PLAY/PAUSE on your IR-Remote several times')
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
		xbmcgui.Dialog().ok("Configuration of remote control", "Your remote has been successfully configured!")
		os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/en/end_en.py\")'")

	else:
		conffile = open("/storage/.config/rc_maps.cfg", "w")
		conffile.write("")
		conffile.close()

		remotefile = open("/storage/.config/rc_keymaps/my_custom_remote","w")
		remotefile.write ("")
		remotefile.close()
		os.system("rm /storage/.kodi/temp/my_custom_remote")
		xbmcgui.Dialog().ok("Configuration of remote control", "Cancelled! Configuration aborted!")
		os.system("kodi-send --action='RunScript(\"/storage/.kodi/addons/service.autoexec/resources/en/end_en.py\")'")

	break
