import time
import log
import sys
import pytz
import settings
import datetime
import signal
import sun
import RPi.GPIO as GPIO


def initGPIO():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(settings.GPIO_1_OUT_PIN, GPIO.OUT, initial=1)
	GPIO.setup(settings.GPIO_2_OUT_PIN, GPIO.OUT, initial=1)


def uninitGPIO():
	setOff1()
	setOff2()
	GPIO.cleanup()


def setOn1():
	log.Add( log.LEVEL_INFO, "Output 1 On" )
	GPIO.output(settings.GPIO_1_OUT_PIN, 0)


def setOn2():
	log.Add( log.LEVEL_INFO, "Output 2 On" )
	GPIO.output(settings.GPIO_2_OUT_PIN, 0)


def setOff1():
	log.Add( log.LEVEL_INFO, "Output 1 Off" )
	GPIO.output(settings.GPIO_1_OUT_PIN, 1)


def setOff2():
	log.Add( log.LEVEL_INFO, "Output 2 Off" )
	GPIO.output(settings.GPIO_2_OUT_PIN, 1)


def getLocalDateTime():
	tz = pytz.timezone( settings.TIME_ZONE )
	t = tz.localize( datetime.datetime.now() )
	return t


def getSunriseSunset( localDateTime ):
	s = sun.sun( lat = settings.LATITUDE, long = settings.LONGITUDE )
	sunset = s.sunset(localDateTime)
	sunrise = s.sunrise(localDateTime)
	result = {}
	result["sunrise"] = sunrise
	result["sunset"] = sunset
	return result


def isSunUp( localDateTime, sunriseSunset ):
	s = getSunriseSunset(localDateTime)
	t = localDateTime.time()
	log.Add( log.LEVEL_INFO, "Sunset: {}, Sunrise: {}, Now: {}".format( sunriseSunset["sunset"], sunriseSunset["sunrise"], t ) )
	if t > sunriseSunset["sunset"] and t < sunriseSunset["sunrise"]:
		return True
	else:
		return False


def timeDiffSunset(localDateTime, sunriseSunset):
	dtSun = datetime.datetime.combine( datetime.date.today(), sunriseSunset["sunset"])
	tz = pytz.timezone( settings.TIME_ZONE )
	t = tz.localize( dtSun )
	sunUp = isSunUp(localDateTime, sunriseSunset)
	return t - localDateTime
	

def updateSwitch():
	dt = getLocalDateTime()
	s = getSunriseSunset(dt)
	sunUp = isSunUp(dt, s)
	diffSunset = timeDiffSunset(dt, s)
	if sunUp:
		log.Add( log.LEVEL_INFO, "Sun is up" )
	else:
		log.Add( log.LEVEL_INFO, "Sun is down" )
	log.Add( log.LEVEL_INFO, "Timediff to sunset: {}, sec: {}".format(diffSunset, diffSunset.total_seconds()) )


def main():
	initGPIO()
	try:
		while True:
			setOn1()
			#setOff2()
			#time.sleep(3)
			#setOff1()
			setOn2()
			time.sleep(3)

		while True:
			updateSwitch()
			time.sleep(settings.UPDATE_INTERVAL_SEC)

	except:
		pass

	uninitGPIO()		
	return 0


if __name__ == "__main__":
	log.Add( log.LEVEL_INFO, "Starting" )
	ret = main()
	log.Add( log.LEVEL_INFO, "Done" )
	sys.exit(ret)

