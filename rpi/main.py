import time
import log
import relay
import externalifc
import timer
import sys
import settings
import threading
import wifi
import datetime
from sunrise_sunset import SunriseSunset


_manualOverride = False


def _cbExtIfcOn( req ):
	global _manualOverride
	_manualOverride = True
	log.add( log.LEVEL_INFO, "Manual switch ON" )
	relay.setOn()
	return "OK"


def _cbExtIfcOff( req ):
	global _manualOverride
	_manualOverride = True
	log.add( log.LEVEL_INFO, "Manual switch OFF" )
	relay.setOff()
	return "OK"


def _cbExtIfcTimer( req ):
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


def _cbExtIfcState( req ):
	rsp = ""
	isOn = relay.isOn()
	periods = timer.activePeriods()
	periodsStr = ""
	if "timer" in periods:
		periodsStr += ";TIMERACTIVE={};TIMERSTART={};TIMERSTOP={}".format(
			periods["timer"]["active"], periods["timer"]["start"].isoformat(),
			periods["timer"]["stop"].isoformat() )
	if "sunrise" in periods:
		# add Z to indicate UTC date time in ISO format
		periodsStr += ";SUNRISEACTIVE={};SUNRISESTART={}Z;SUNRISESTOP={}Z".format( 
			periods["sunrise"]["active"], periods["sunrise"]["start"].isoformat(), periods["sunrise"]["stop"].isoformat() )
	if "sunset" in periods:
		periodsStr += ";SUNSETACTIVE={};SUNSETSTART={}Z;SUNSETSTOP={}Z".format( 
			periods["sunset"]["active"], periods["sunset"]["start"].isoformat(), periods["sunset"]["stop"].isoformat() )
	periodsStr = periodsStr.upper()
	if _manualOverride:
		if isOn:
			rsp = "SWITCH=ON" + periodsStr
		else:
			rsp = "SWITCH=OFF" + periodsStr
	else:
		if isOn:
			rsp = "SWITCH=TIMER;STATE=ON" + periodsStr
		else:
			rsp = "SWITCH=TIMER;STATE=OFF" + periodsStr
	return rsp

def _cbExtIfcGetSettings( req ):
	log.add( log.LEVEL_DEBUG, "Get settings" )
	rsp = settings.toString()
	return rsp

def _cbExtIfcSetSettings( req ):
	log.add( log.LEVEL_DEBUG, "Set settings" )
	# strip starting SETTINGS;
	settingsStr = req[ len( "SETTINGS;" ): ]
	settings.fromString( settingsStr )
	return "OK"

def _cbExtIfcSun( req ):
	log.add( log.LEVEL_DEBUG, "Req. sun info" )
	now = datetime.datetime.utcnow()
	sunriseToday, sunsetToday = SunriseSunset(now, latitude = settings.getLatitude(), longitude = settings.getLongitude()).calculate()
	rsp = "SUNRISE={}Z;SUNSET={}Z".format( sunriseToday.isoformat(), sunsetToday.isoformat() )
	return rsp
	

def _updateSwitch():
	if not _manualOverride:
		if timer.active():
			log.add( log.LEVEL_INFO, "Timer ON" )
			relay.setOn()
		else:
			log.add( log.LEVEL_INFO, "Timer OFF" )
			relay.setOff()
	threading.Timer(settings.getUpdateTimerIntervalSec(), _updateSwitch).start()


def _checkWifi():
	if not wifi.check():
		wifi.restart()
	threading.Timer(settings.getCheckWifiIntervalSec(), _checkWifi).start()


def main():
	# setup callback dictionary
	cb = { "on" : _cbExtIfcOn,
		"off" : _cbExtIfcOff,
		"timer" : _cbExtIfcTimer,
		"state" : _cbExtIfcState,
		"settings" : _cbExtIfcGetSettings,
		"set_settings" : _cbExtIfcSetSettings,
		"sun" : _cbExtIfcSun
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
	settings.init()
	log.add( log.LEVEL_INFO, "Starting" )
	ret = main()
	log.add( log.LEVEL_INFO, "Done" )
	sys.exit(ret)

