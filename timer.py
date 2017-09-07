import log
import pytz
import settings
import datetime
import sun


def _getLocalDateTime():
	tz = pytz.timezone( settings.TIME_ZONE )
	dt = datetime.datetime.now()
	result = tz.localize( dt )
	return result


def _getSunriseSunset( localDateTime ):
	s = sun.sun( lat = settings.LATITUDE, long = settings.LONGITUDE )
	sunrise = s.sunrise(localDateTime)
	noon = s.solarnoon(localDateTime)
	sunset = s.sunset(localDateTime)
	result = {}
	result["sunrise"] = sunrise
	result["noon"] = noon
	result["sunset"] = sunset
	return result


def _isSunUp( localDateTime, sunriseSunset ):
	t = localDateTime.time()
	sr = sunriseSunset["sunrise"]
	sn = sunriseSunset["noon"]
	ss = sunriseSunset["sunset"]
	log.Add( log.LEVEL_DEBUG, "Sunrise: {}, Noon: {}, Sunset: {}, Now: {}".format( sr, sn, ss, t ) )
	result = True
	if sn >= sr:
		if sn <= ss:
			result = t > sr and t < ss
		else:
			result = t > sr or t < ss
	else:
		result = t > sr or t < ss
	return result


def _timeUntilSunset( localDateTime, sunriseSunset ):
	t = localDateTime.time()
	ssTime = sunriseSunset["sunset"]
	ss = None
	if ssTime < t:
		# sunset tomorrow
		ss = datetime.datetime.combine( localDateTime.date() + datetime.timedelta( days = 1), ssTime )
	else:
		ss = datetime.datetime.combine( localDateTime.date(), ssTime )

	tz = pytz.timezone( settings.TIME_ZONE )
	ss = tz.localize( ss )
	return (ss - localDateTime)


def _timeAfterSunset( localDateTime, sunriseSunset ):
	t = localDateTime.time()
	ssTime = sunriseSunset["sunset"]
	ss = None
	if ssTime > t:
		# sunset yesterday
		ss = datetime.datetime.combine( localDateTime.date() - datetime.timedelta( days = 1), ssTime )
	else:
		ss = datetime.datetime.combine( localDateTime.date(), ssTime )

	tz = pytz.timezone( settings.TIME_ZONE )
	ss = tz.localize( ss )
	return (localDateTime - ss)


def _checkActiveEnd( localDateTime, sunriseSunset ):
	# try to figure out when active period begun
	tActivate = (datetime.datetime.combine(localDateTime.date(), sunriseSunset["sunset"]) + settings.ON_TIME_DIFF_SUNSET).time()
	dtActivate = datetime.datetime.combine( localDateTime.date(), tActivate )
	tz = pytz.timezone( settings.TIME_ZONE )
	dtActivate = tz.localize( dtActivate )
	if dtActivate > localDateTime:
		# yesterday
		dtActivate = dtActivate - datetime.timedelta( days = 1 )
	log.Add( log.LEVEL_DEBUG, "Active period started {}".format(dtActivate) )
	wDay = dtActivate.weekday()
	tEnd = settings.OFF_TIME_DAY_LIST[wDay]
	dtEnd = datetime.datetime.combine( dtActivate.date(), tEnd )
	if tEnd < tActivate:
		# end day after activate
		dtEnd = dtEnd + datetime.timedelta( days = 1 )
	dtEnd = tz.localize( dtEnd ) 
	log.Add( log.LEVEL_DEBUG, "Active period off time {}".format(dtEnd) )
	return localDateTime >= dtEnd


def active():
	dt = _getLocalDateTime()
	s = _getSunriseSunset(dt)
	sunUp = _isSunUp(dt, s)
	ssDiffSec = 0
	if sunUp:
		ssDiff = _timeUntilSunset(dt, s)
		ssDiffSec = -1 * ssDiff.total_seconds()
		log.Add( log.LEVEL_DEBUG, "Sun is up, time before sunset {}".format(ssDiff) )
	else:
		ssDiff = _timeAfterSunset(dt, s)
		ssDiffSec = ssDiff.total_seconds()
		log.Add( log.LEVEL_DEBUG, "Sun is down, time after sunset {}".format(ssDiff) )
	
	activeDiffSec = settings.ON_TIME_DIFF_SUNSET.total_seconds()
	if activeDiffSec < 0:
		log.Add( log.LEVEL_DEBUG, "Timer shall be active {} sec. before sunset".format(-1 * activeDiffSec) )
	else:
		log.Add( log.LEVEL_DEBUG, "Timer shall be active {} sec. after sunset".format(activeDiffSec) )
	active = ssDiffSec >= settings.ON_TIME_DIFF_SUNSET.total_seconds()
	
	# if active check if active period has ended
	if active:
		active = not _checkActiveEnd(dt, s)
		
	return active

if __name__ == "__main__":
	ret = active()
	if ret:
		log.Add( log.LEVEL_INFO, "Timer active" )
	else:
		log.Add( log.LEVEL_INFO, "Timer inactive" )
