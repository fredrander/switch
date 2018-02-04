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
	rsp = "SETTINGS;LATITUDE={};LONGITUDE={};TIME_ZONE={};".format( settings.getLatitude(), settings.getLongitude(), settings.getTimeZone() )
	rsp += "SUNSET={};SUNSET_ON_DIFF_MINUTES={};".format( settings.getSunsetEnabled(), int( settings.getSunsetOnTimeDelta().total_seconds() / 60 ) ).upper()
	rsp += "SUNSET_OFF_MON={};SUNSET_OFF_TUE={};SUNSET_OFF_WED={};SUNSET_OFF_THU={};".format( settings.getSunsetOffTime( 0 ), 
		settings.getSunsetOffTime( 1 ), settings.getSunsetOffTime( 2 ), settings.getSunsetOffTime( 3 ) )
	rsp += "SUNSET_OFF_FRI={};SUNSET_OFF_SAT={};SUNSET_OFF_SUN={};".format( settings.getSunsetOffTime( 4 ), 
		settings.getSunsetOffTime( 5 ), settings.getSunsetOffTime( 6 ) )
	rsp += "SUNRISE={};SUNRISE_OFF_DIFF_MINUTES={};".format( settings.getSunriseEnabled(), int( settings.getSunriseOffTimeDelta().total_seconds() / 60 ) ).upper()
	rsp += "SUNRISE_ON_MON={};SUNRISE_ON_TUE={};SUNRISE_ON_WED={};SUNRISE_ON_THU={};".format( settings.getSunriseOnTime( 0 ), 
		settings.getSunriseOnTime( 1 ), settings.getSunriseOnTime( 2 ), settings.getSunriseOnTime( 3 ) )
	rsp += "SUNRISE_ON_FRI={};SUNRISE_ON_SAT={};SUNRISE_ON_SUN={}".format( settings.getSunriseOnTime( 4 ), 
		settings.getSunriseOnTime( 5 ), settings.getSunriseOnTime( 6 ) )
	return rsp

def _cbExtIfcSetSettings( req ):
	log.add( log.LEVEL_DEBUG, "Set settings" )
	reqList = req.split( ";" )
	for s in reqList:
		settingsPair = s.split( "=" )
		if ( len( settingsPair ) == 2 ):
			if ( settingsPair[ 0 ] == "LATITUDE" ):
				settings.setLatitude( settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "LONGITUDE" ):
				settings.setLongitude( settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "TIME_ZONE" ):
				tzStr = settingsPair[ 1 ].replace( "\\", "/" ) 
				settings.setTimeZone( tzStr )
			elif ( settingsPair[ 0 ] == "SUNRISE" ):
				boolStr = settingsPair[ 1 ].lower()
				settings.setSunriseEnabled( boolStr )
			elif ( settingsPair[ 0 ] == "SUNRISE_OFF_DIFF_MINUTES" ):
				settings.setSunriseOffTimeDelta( settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNRISE_ON_MON" ):
				settings.setSunriseOnTime( "mon", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNRISE_ON_TUE" ):
				settings.setSunriseOnTime( "tue", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNRISE_ON_WED" ):
				settings.setSunriseOnTime( "wed", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNRISE_ON_THU" ):
				settings.setSunriseOnTime( "thu", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNRISE_ON_FRI" ):
				settings.setSunriseOnTime( "fri", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNRISE_ON_SAT" ):
				settings.setSunriseOnTime( "sat", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNRISE_ON_SUN" ):
				settings.setSunriseOnTime( "sun", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNSET" ):
				boolStr = settingsPair[ 1 ].lower()
				settings.setSunsetEnabled( boolStr )
			elif ( settingsPair[ 0 ] == "SUNSET_ON_DIFF_MINUTES" ):
				settings.setSunsetOnTimeDelta( settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNSET_OFF_MON" ):
				settings.setSunsetOffTime( "mon", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNSET_OFF_TUE" ):
				settings.setSunsetOffTime( "tue", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNSET_OFF_WED" ):
				settings.setSunsetOffTime( "wed", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNSET_OFF_THU" ):
				settings.setSunsetOffTime( "thu", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNSET_OFF_FRI" ):
				settings.setSunsetOffTime( "fri", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNSET_OFF_SAT" ):
				settings.setSunsetOffTime( "sat", settingsPair[ 1 ] )
			elif ( settingsPair[ 0 ] == "SUNSET_OFF_SUN" ):
				settings.setSunsetOffTime( "sun", settingsPair[ 1 ] )
	settings.write()
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

