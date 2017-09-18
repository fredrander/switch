import time
import log
import relay
import externalifc
import timer
import sys
import settings
import threading
import wifi


_manualOverride = False


def _cbExtIfcOn():
	global _manualOverride
	_manualOverride = True
	log.add( log.LEVEL_INFO, "Manual switch ON" )
	relay.setOn()
	return "OK"


def _cbExtIfcOff():
	global _manualOverride
	_manualOverride = True
	log.add( log.LEVEL_INFO, "Manual switch OFF" )
	relay.setOff()
	return "OK"


def _cbExtIfcTimer():
	global _manualOverride
	_manualOverride = False
	log.add( log.LEVEL_INFO, "Timer mode ON" )
	if timer.active():
		log.add( log.LEVEL_INFO, "Timer ON" )
		relay.setOn()
	else:
		log.add( log.LEVEL_INFO, "Timer OFF" )
		relay.setOff()
	return "OK"


def _cbExtIfcState():
	rsp = ""
	isOn = relay.isOn()
	if _manualOverride:
		if isOn:
			rsp = "SWITCH=ON"
		else:
			rsp = "SWITCH=OFF"
	else:
		if isOn:
			rsp = "SWITCH=TIMER;STATE=ON"
		else:
			rsp = "SWITCH=TIMER;STATE=OFF"
	return rsp


def _updateSwitch():
	if not _manualOverride:
		if timer.active():
			log.add( log.LEVEL_INFO, "Timer ON" )
			relay.setOn()
		else:
			log.add( log.LEVEL_INFO, "Timer OFF" )
			relay.setOff()
	threading.Timer(settings.UPDATE_INTERVAL_SEC, _updateSwitch).start()


def _checkWifi():
	if not wifi.check():
		wifi.restart()
	threading.Timer(settings.CHECK_WIFI_INTERVAL_SEC, _checkWifi).start()


def main():
	# setup callback dictionary
	cb = { "on" : _cbExtIfcOn,
		"off" : _cbExtIfcOff,
		"timer" : _cbExtIfcTimer,
		"?" : _cbExtIfcState 
	}
	externalifc.init( cb )
	relay.init()
	_updateSwitch()
	_checkWifi()
	while True:
		time.sleep(999)
	relay.done()		
	return 0


if __name__ == "__main__":
	log.add( log.LEVEL_INFO, "Starting" )
	ret = main()
	log.add( log.LEVEL_INFO, "Done" )
	sys.exit(ret)

