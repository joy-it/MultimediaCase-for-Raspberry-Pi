import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')
from gpiozero import CPUTemperature, PWMLED
from time import sleep

led = PWMLED(17) # PWM-Pin

startTemp = 60.0 # Temperatur bei der der Luefter an geht
coolDown = 50.0  # Temperatur zu der heruntergekuehlt wird
active_coolDown = False # Variable zum herunterkuehlen

pTemp = 8 # Proportionalanteil
iTemp = 0.2 # Integralanteil

fanSpeed = 0 # Lueftergeschwindigkeit
sum = 0 # Speichervariable fur iAnteil


while True: # Regelschleife
 cpu = CPUTemperature() # Auslesen der aktuellen Temperaturwerte
 actTemp = cpu.temperature # Aktuelle Temperatur als float-Variable

 if actTemp < coolDown:
  active_coolDown = False # nicht kuehlen
 elif actTemp > startTemp:
  active_coolDown = True # kuehlen
  
 diff = actTemp - startTemp
 sum = sum + diff
 pDiff = diff * pTemp
 iDiff = sum * iTemp
 
 if active_coolDown == True: # Geschwindigkeit des Luefters anpassen
  fanSpeed = pDiff + iDiff + 35
  while(fanSpeed < 45 and active_coolDown == True): 
   fanSpeed = fanSpeed + 1
   
 elif active_coolDown == False: # Luefter auf Null setzen
  fanSpeed = 0

 # Randwerte setzen
 if fanSpeed > 100:
  fanSpeed = 100
 if sum > 100 :
  sum = 100
 elif sum < -100:
  sum = -100

 led.value = fanSpeed / 100 # PWM Ausgabe
 sleep(1) 