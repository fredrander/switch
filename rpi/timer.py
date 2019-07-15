import log
import pytz
import settings
import datetime
import calendar
from sunrise_sunset import SunriseSunset


def _utc2Local( tmUtc ):
	tzLocal = pytz.timezone( settings.getTimeZone() )
	tzUtc = pytz.utc
	result = tmUtc
	# make date/time aware that it is UTC
	result = result.replace( tzinfo=tzUtc )
	result = result.astimezone( tzLocal )
	# remove TZ awareness
	result = result.replace( tzinfo=None )
	return result

def _local2utc( tm ):
	tzLocal = pytz.timezone( settings.getTimeZone() )
	tzUtc = pytz.utc
	result = tm
	# make date/time aware that it is local
	result = result.replace( tzinfo=tzLocal )
	result = result.astimezone( tzUtc )
	# remove TZ awareness
	result = result.replace( tzinfo=None )
	return result

def _getRelevantSunriseSunset( now ):
	# calculate sunrise/sunset for today, tomorrow and yesterday
	sunriseToday, sunsetToday = SunriseSunset(now, latitude = settings.getLatitude(), longitude = settings.getLongitude()).calculate()
	sunriseTomorrow, sunsetTomorrow = SunriseSunset(now + datetime.timedelta( days=1 ), latitude = settings.getLatitude(), longitude = settings.getLongitude()).calculate()
	sunriseYesterday, sunsetYesterday = SunriseSunset(now - datetime.timedelta( days=1 ), latitude = settings.getLatitude(), longitude = settings.getLongitude()).calculate()

	# use sunrise for tomorrow if we have passed stop trigger for today
	if now >= sunriseToday + settings.getSunriseOffTimeDelta():
		sunrise = sunriseTomorrow
	else:
		sunrise = sunriseToday
	# use sunset from yesterday if we have not passed start trigger for today
	if now < sunsetToday + settings.getSunsetOnTimeDelta():
		sunset = sunsetYesterday
	else:
		sunset = sunsetToday
	
	return sunrise, sunset


def _getOnPeriodSunset( sunset ):
	# start based on sunset
	start = sunset + settings.getSunsetOnTimeDelta()
	stopLocalTime = settings.getSunsetOffTime( start.weekday() )
	stop = datetime.datetime.combine( start.date(), stopLocalTime )
	# convert local to UTC
	stop = _local2utc(stop)
	
	# check if stop next day
	if stop < start and stopLocalTime <= datetime.time(12):
		log.add(log.LEVEL_TRACE, "Stop time past midnight, add one day to stop: {} --> {}".format(stop, stop + datetime.timedelta( days=1 )) )
		stop = stop + datetime.timedelta( days=1 )
	return start, stop


def _getOnPeriodSunrise( sunrise ):
	# stop based on sunrise
	stop = sunrise + settings.getSunriseOffTimeDelta()
	startLocalTime = settings.getSunriseOnTime( stop.weekday() )
	start = datetime.datetime.combine( stop.date(), startLocalTime )
	# convert local to UTC
	start = _local2utc(start)
	# check if prev day
	if stop < start and startLocalTime > datetime.time(12):
		log.add(log.LEVEL_TRACE, "Start time past midnight, decrease start with one day: {} --> {}".format(start, start - datetime.timedelta( days=1 )) )
		start = start - datetime.timedelta( days=1 )
	return start, stop

def _getOnPeriodTimer( now ):
	nextStart = datetime.datetime(2000, 1, 1, 0, 0)
	nextStop = datetime.datetime(2000, 1, 1, 0, 0)
	for i in range( 1, 9 ):
		intervalOn = settings.getTimerOnTime( i )
		intervalOff = settings.getTimerOffTime( i )
		intervalDays = settings.getTimerDays( i )
		dateTimeOn = datetime.datetime.combine( now.date(), intervalOn )
		dateTimeOff = datetime.datetime.combine( now.date(), intervalOff )
		if dateTimeOn > dateTimeOff:
			dateTimeOff += datetime.timedelta( days=1 )
			if now < dateTimeOn:
				dateTimeOn -= datetime.timedelta( days=1 )
				dateTimeOff -= datetime.timedelta( days=1 )
		if ( intervalDays & ( 1 << dateTimeOn.weekday() ) ) != 0:
			if now >= dateTimeOn and now <= dateTimeOff:
				return dateTimeOn, dateTimeOff
			elif nextStart == None:
				nextStart = dateTimeOn
				nextStop = dateTimeOff
			elif ( dateTimeOn > now and ( dateTimeOn < nextStart or nextStart < now ) ):
				nextStart = dateTimeOn
				nextStop = dateTimeOff

	return nextStart, nextStop

def activePeriods( nowUtc = None ):
	# get current date/time
	now = nowUtc
	if not now:
		now = datetime.datetime.utcnow()
	nowLocal = _utc2Local( now )

	result = {}

	# check timer periods (timer works in local timezone)
	if settings.getTimerEnabled():
		startTimer, stopTimer = _getOnPeriodTimer( nowLocal )
		log.add(log.LEVEL_DEBUG, "Now: {} {}, Timer On: {}, Timer Off: {}".format( calendar.day_abbr[nowLocal.weekday()], nowLocal, startTimer, stopTimer))
		if nowLocal >= startTimer and nowLocal <= stopTimer:
			result["timer"] = { "active" : True, "start" : startTimer, "stop" : stopTimer }
		else:
			result["timer"] = { "active" : False, "start" : startTimer, "stop" : stopTimer }

	# get sunrise/sunset
	sunrise, sunset = _getRelevantSunriseSunset( now )
	log.add(log.LEVEL_DEBUG, "Now: {} {} UTC, Sunrise: {} UTC, Sunset: {} UTC".format( calendar.day_abbr[now.weekday()], now, sunrise, sunset))
	# get timer start/stop at sunset
	startSunset, stopSunset = _getOnPeriodSunset( sunset )
	# get timer start/stop at sunrise
	startSunrise, stopSunrise = _getOnPeriodSunrise( sunrise )
	if settings.getSunsetEnabled():
		log.add(log.LEVEL_DEBUG, "Active period at sunset, start: {} UTC, stop: {} UTC".format(startSunset, stopSunset))
		if now >= startSunset and now < stopSunset:
			log.add( log.LEVEL_DEBUG, "Timer active at sunset" )
			result["sunset"] = { "active" : True, "start" : startSunset, "stop" : stopSunset }
		else:
			log.add( log.LEVEL_DEBUG, "Timer inactive at sunset" )
			result["sunset"] = { "active" : False, "start" : startSunset, "stop" : stopSunset }

	if settings.getSunriseEnabled():
		log.add(log.LEVEL_DEBUG, "Active period at sunrise, start: {} UTC, stop: {} UTC".format(startSunrise, stopSunrise))
		if now >= startSunrise and now < stopSunrise:
			log.add( log.LEVEL_DEBUG, "Timer active at sunrise" )
			result["sunrise"] = { "active" : True, "start" : startSunrise, "stop" : stopSunrise }
		else:
			log.add( log.LEVEL_DEBUG, "Timer inactive at sunrise" )
			result["sunrise"] = { "active" : False, "start" : startSunrise, "stop" : stopSunrise }
	return result


def active( nowUtc = None ):
	# get active periods
	periods = activePeriods( nowUtc )
	result = False
	if "timer" in periods:
		result = result or periods["timer"]["active"]
	if "sunset" in periods:
		result = result or periods["sunset"]["active"]
	if "sunrise" in periods:
		result = result or periods["sunrise"]["active"]
	return result


if __name__ == "__main__":

	settings.init()
	now = datetime.datetime.now()
	timerOn, trimerOff = _getOnPeriodTimer( now )
	print( "TIMER: {} --> {}".format( timerOn, trimerOff ) )
