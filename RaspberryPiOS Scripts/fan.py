from gpiozero import CPUTemperature, PWMLED
from time import sleep

led = PWMLED(17) # PWM-Pin

startTemp = 60.0 # Temperature at which the fan goes on
coolDown = 50.0  # Temperature to which it is cooled down
active_coolDown = False # Variable to cool down

pTemp = 8 # Proportional part
iTemp = 0.2 # Integral part

fanSpeed = 0 # Fan speed
sum = 0 # Memory variable for ishare

while True: # control loop
	cpu = CPUTemperature() # Reading the current temperature
	actTemp = cpu.temperature # Current temperature as float variable

	if actTemp < coolDown:
		active_coolDown = False # do not cool
	elif actTemp > startTemp:
		active_coolDown = True # cool

	diff = actTemp - startTemp
	sum = sum + diff
	pDiff = diff * pTemp
	iDiff = sum * iTemp

	if active_coolDown == True: # Adjust fan speed
		fanSpeed = pDiff + iDiff + 35

		while(fanSpeed < 45 and active_coolDown == True):
			fanSpeed = fanSpeed + 1
	elif active_coolDown == False: # Set fan to zero
		fanSpeed = 0

	# Set boundary values
	if fanSpeed > 100:
		fanSpeed = 100
	if sum > 100 :
		sum = 100
	elif sum < -100:
		sum = -100

	# print(str(actTemp) + " *C, " + str(fanSpeed))		# Printing temperature and teh speed of the fan
	led.value = fanSpeed / 100 # PWM output
	sleep(1)
