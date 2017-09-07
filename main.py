import time
import log
import relay
import externalifc
import timer
import sys
import settings


_manualOverride = False


def _cbExtIfcOn():
	global _manualOverride
	_manualOverride = True
	log.Add( log.LEVEL_INFO, "Manual switch ON" )
	relay.setOn1()


def _cbExtIfcOff():
	global _manualOverride
	_manualOverride = True
	log.Add( log.LEVEL_INFO, "Manual switch OFF" )
	relay.setOff1()


def main():
	externalifc.init( _cbExtIfcOn, _cbExtIfcOff )
	relay.init()
	relay.setOff2()
	while True:
		if not _manualOverride:
			if timer.active():
				log.Add( log.LEVEL_INFO, "Timer ON" )
				relay.setOn1()
			else:
				log.Add( log.LEVEL_INFO, "Timer OFF" )
				relay.setOff1()
		time.sleep(settings.UPDATE_INTERVAL_SEC)
	relay.done()		
	return 0


if __name__ == "__main__":
	log.Add( log.LEVEL_INFO, "Starting" )
	ret = main()
	log.Add( log.LEVEL_INFO, "Done" )
	sys.exit(ret)
