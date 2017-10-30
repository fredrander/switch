import log
import pytz
import settings
import datetime
import calendar
from sunrise_sunset import SunriseSunset


def _getRelevantSunriseSunset( now ):
	# calculate sunrise/sunset for today, tomorrow and yesterday
	sunriseToday, sunsetToday = SunriseSunset(now, latitude = settings.LATITUDE, longitude = settings.LONGITUDE).calculate()
	sunriseTomorrow, sunsetTomorrow = SunriseSunset(now + datetime.timedelta( days=1 ), latitude = settings.LATITUDE, longitude = settings.LONGITUDE).calculate()
	sunriseYesterday, sunsetYesterday = SunriseSunset(now - datetime.timedelta( days=1 ), latitude = settings.LATITUDE, longitude = settings.LONGITUDE).calculate()

	# use sunrise for tomorrow if we have passed stop trigger for today
	if now >= sunriseToday + settings.SUNRISE_OFF_TIME_DIFF:
		sunrise = sunriseTomorrow
	else:
		sunrise = sunriseToday
	# use sunset from yesterday if we have not passed start trigger for today
	if now < sunsetToday + settings.SUNSET_ON_TIME_DIFF:
		sunset = sunsetYesterday
	else:
		sunset = sunsetToday
	
	return sunrise, sunset


def _getOnPeriodSunset( sunset ):
	# start based on sunset
	start = sunset + settings.SUNSET_ON_TIME_DIFF
	stopLocalTime = settings.SUNSET_OFF_TIME_DAY_LIST[start.weekday()]
	stop = datetime.datetime.combine( start.date(), stopLocalTime )
	# convert local to UTC
	tz = pytz.timezone(settings.TIME_ZONE)
	stop = tz.localize(stop, is_dst=None).astimezone(pytz.utc).replace(tzinfo=None)
	
	# check if stop next day
	if stop < start and stopLocalTime <= datetime.time(12):
		log.add(log.LEVEL_TRACE, "Stop time past midnight, add one day to stop: {} --> {}".format(stop, stop + datetime.timedelta( days=1 )) )
		stop = stop + datetime.timedelta( days=1 )
	return start, stop


def _getOnPeriodSunrise( sunrise ):
	# stop based on sunrise
	stop = sunrise + settings.SUNRISE_OFF_TIME_DIFF
	startLocalTime = settings.SUNRISE_ON_TIME_DAY_LIST[stop.weekday()]
	start = datetime.datetime.combine( stop.date(), startLocalTime )
	# convert local to UTC
	tz = pytz.timezone (settings.TIME_ZONE)
	start = tz.localize(start, is_dst=None).astimezone(pytz.utc).replace(tzinfo=None)
	# check if prev day
	if stop < start and startLocalTime > datetime.time(12):
		log.add(log.LEVEL_TRACE, "Start time past midnight, decrease start with one day: {} --> {}".format(start, start - datetime.timedelta( days=1 )) )
		start = start - datetime.timedelta( days=1 )
	return start, stop


def activePeriods( nowUtc = None ):
	# get current date/time
	now = nowUtc
	if not now:
		now = datetime.datetime.utcnow()
	# get sunrise/sunset
	sunrise, sunset = _getRelevantSunriseSunset( now )
	log.add(log.LEVEL_DEBUG, "Now: {} {} UTC, Sunrise: {} UTC, Sunset: {} UTC".format( calendar.day_abbr[now.weekday()], now, sunrise, sunset))
	# get timer start/stop at sunset
	startSunset, stopSunset = _getOnPeriodSunset( sunset )
	# get timer start/stop at sunrise
	startSunrise, stopSunrise = _getOnPeriodSunrise( sunrise )
	result = {}
	if settings.SUNSET_TIMER_ACTIVE:
		log.add(log.LEVEL_DEBUG, "Active period at sunset, start: {} UTC, stop: {} UTC".format(startSunset, stopSunset))
		if now >= startSunset and now < stopSunset:
			log.add( log.LEVEL_DEBUG, "Timer active at sunset" )
			result["sunset"] = { "active" : True, "start" : startSunset, "stop" : stopSunset }
		else:
			log.add( log.LEVEL_DEBUG, "Timer inactive at sunset" )
			result["sunset"] = { "active" : False, "start" : startSunset, "stop" : stopSunset }

	if settings.SUNRISE_TIMER_ACTIVE:
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
	if "sunset" in periods:
		result = result or periods["sunset"]["active"]
	if "sunrise" in periods:
		result = result or periods["sunrise"]["active"]
	return result


if __name__ == "__main__":
	log.setLevel(log.LEVEL_DEBUG)
	log.add( log.LEVEL_INFO, "=========== Timer test start ===========" )
	start = datetime.datetime.utcnow()
	#start = datetime.datetime(2017,5,11)
	stop = start# + datetime.timedelta( days=365 )
	step = datetime.timedelta( hours=4 )
	curr = start
	while curr <= stop:
		ret = active(curr)
		if ret:
			log.add( log.LEVEL_INFO, "Timer active" )
		else:
			log.add( log.LEVEL_INFO, "Timer inactive" )
		curr = curr + step
	log.add( log.LEVEL_INFO, "Timer test stop" )
