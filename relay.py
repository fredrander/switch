import log
import settings
import RPi.GPIO as GPIO


def init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(settings.GPIO_1_OUT_PIN, GPIO.OUT)
	GPIO.setup(settings.GPIO_2_OUT_PIN, GPIO.OUT)


def done():
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
