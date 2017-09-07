import time
import log
import relay
import timer
import sys
import settings


def main():
	relay.init()
	relay.setOff2()
	while True:
		if timer.active():
			relay.setOn1()
		else:
			relay.setOff1()
		time.sleep(settings.UPDATE_INTERVAL_SEC)
	relay.done()		
	return 0


if __name__ == "__main__":
	log.Add( log.LEVEL_INFO, "Starting" )
	ret = main()
	log.Add( log.LEVEL_INFO, "Done" )
	sys.exit(ret)

