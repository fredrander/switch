import log
import settings
import RPi.GPIO as GPIO


def _setOut( p, state ):
	log.add( log.LEVEL_DEBUG, "Set pin {} to state {}".format( p, state ) )
	GPIO.output( p, state )

 
def init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	for p in settings.GPIO_CONTROLLED_OUT_PINS:
		GPIO.setup(p, GPIO.OUT)


def done():
	setOff()
	GPIO.cleanup()


def setOn():
	for p in settings.GPIO_CONTROLLED_OUT_PINS:
		_setOut( p, 0 )


def setOff():
	for p in settings.GPIO_CONTROLLED_OUT_PINS:
		_setOut( p, 1 )


def isOn():
	pinValue = 0
	for p in settings.GPIO_CONTROLLED_OUT_PINS:
		pinValue = GPIO.input( p )
	if pinValue == 0:
		return True
	else:
		return False

