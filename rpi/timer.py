import log
import pytz
import settings
import datetime
import calendar
from sunrise_sunset import SunriseSunset


def _nearestDateTime( dateTime, candidates ):
	best = None
	bestAbsDiffSec = None
	for c in candidates:
		absDiffSec = abs( (c - dateTime).total_seconds() )
		if not bestAbsDiffSec or absDiffSec < bestAbsDiffSec:
			bestAbsDiffSec = absDiffSec
			best = c
	return best

	
def _getSunriseSunset( now ):
	# calculate sunrise/sunset for today, tomorrow and yesterday
	sunriseToday, sunsetToday = SunriseSunset(now, latitude = settings.LATITUDE, longitude = settings.LONGITUDE).calculate()
	sunriseTomorrow, sunsetTomorrow = SunriseSunset(now + datetime.timedelta( days=1 ), latitude = settings.LATITUDE, longitude = settings.LONGITUDE).calculate()
	sunriseYesterday, sunsetYesterday = SunriseSunset(now - datetime.timedelta( days=1 ), latitude = settings.LATITUDE, longitude = settings.LONGITUDE).calculate()

	# select nearest sunrise/sunset(!)
	sunrise = _nearestDateTime(now, [sunriseToday, sunriseTomorrow, sunriseYesterday])
	sunset = _nearestDateTime(now, [sunsetToday, sunsetTomorrow, sunsetYesterday])
	return sunrise, sunset


def _getOnPeriodSunset( sunset ):
	# start based on sunset
	start = sunset + settings.SUNSET_ON_TIME_DIFF
	weekday = start.weekday()
	stop = datetime.datetime.combine( start.date(), settings.SUNSET_OFF_TIME_DAY_LIST[weekday] )
	# convert local to UTC
	tz = pytz.timezone (settings.TIME_ZONE)
	stop = tz.localize(stop, is_dst=None).astimezone(pytz.utc).replace(tzinfo=None)
	# check if next day
	if stop < start:
		stop = stop + datetime.timedelta( days=1 )
	return start, stop


def _getOnPeriodSunrise( sunrise ):
	# stop based on sunrise
	stop = sunrise + settings.SUNRISE_OFF_TIME_DIFF
	weekday = stop.weekday()
	start = datetime.datetime.combine( stop.date(), settings.SUNRISE_ON_TIME_DAY_LIST[weekday] )
	# convert local to UTC
	tz = pytz.timezone (settings.TIME_ZONE)
	start = tz.localize(start, is_dst=None).astimezone(pytz.utc).replace(tzinfo=None)
	# check if prev day
	if stop < start:
		start = start - datetime.timedelta( days=1 )
	return start, stop


def active( nowUtc = None ):
	# get current date/time
	now = nowUtc
	if not now:
		now = datetime.datetime.utcnow()
	# get sunrise/sunset
	sunrise, sunset = _getSunriseSunset( now )
	log.Add(log.LEVEL_DEBUG, "Now: {} {} UTC, Sunrise: {} UTC, Sunset: {} UTC".format( calendar.day_abbr[now.weekday()], now, sunrise, sunset))
	# get timer start/stop at sunset
	startSunset, stopSunset = _getOnPeriodSunset( sunset )
	log.Add(log.LEVEL_DEBUG, "Active period at sunset, start: {} UTC, stop: {} UTC".format(startSunset, stopSunset))
	# get timer start/stop at sunrise
	startSunrise, stopSunrise = _getOnPeriodSunrise( sunrise )
	log.Add(log.LEVEL_DEBUG, "Active period at sunrise, start: {} UTC, stop: {} UTC".format(startSunrise, stopSunrise))
	result = False
	if settings.SUNSET_TIMER_ACTIVE:
		if now >= startSunset and now < stopSunset:
			log.Add( log.LEVEL_DEBUG, "Timer active at sunset" )
			result = True
		else:
			log.Add( log.LEVEL_DEBUG, "Timer inactive at sunset" )

	if settings.SUNRISE_TIMER_ACTIVE:
		if now >= startSunrise and now < stopSunrise:
			log.Add( log.LEVEL_DEBUG, "Timer active at sunrise" )
			result = True
		else:
			log.Add( log.LEVEL_DEBUG, "Timer inactive at sunrise" )
	return result


if __name__ == "__main__":
	start = datetime.datetime.utcnow()
	stop = start + datetime.timedelta( days=1 )
	step = datetime.timedelta( hours=1 )
	curr = start
	while curr <= stop:
		ret = active(curr)
		if ret:
			log.Add( log.LEVEL_INFO, "Timer active" )
		else:
			log.Add( log.LEVEL_INFO, "Timer inactive" )
		curr = curr + step
