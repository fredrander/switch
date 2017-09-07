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
	log.Add( log.LEVEL_INFO, "Sunrise: {}, Noon: {}, Sunset: {}, Now: {}".format( sr, sn, ss, t ) )
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


def active():
	dt = _getLocalDateTime()
	s = _getSunriseSunset(dt)
	sunUp = _isSunUp(dt, s)
	ssDiffSec = 0
	if sunUp:
		ssDiff = _timeUntilSunset(dt, s)
		ssDiffSec = -1 * ssDiff.total_seconds()
		log.Add( log.LEVEL_INFO, "Sun is up, time before sunset {}".format(ssDiff) )
	else:
		ssDiff = _timeAfterSunset(dt, s)
		ssDiffSec = ssDiff.total_seconds()
		log.Add( log.LEVEL_INFO, "Sun is down, time after sunset {}".format(ssDiff) )
	
	activeDiffSec = settings.ON_TIME_DIFF_SUNSET.total_seconds()
	if activeDiffSec < 0:
		log.Add( log.LEVEL_INFO, "Timer shall be active {} sec. before sunset".format(-1 * activeDiffSec) )
	else:
		log.Add( log.LEVEL_INFO, "Timer shall be active {} sec. after sunset".format(activeDiffSec) )
	active = ssDiffSec >= settings.ON_TIME_DIFF_SUNSET.total_seconds()
	return active

if __name__ == "__main__":
	ret = active()
	if ret:
		log.Add( log.LEVEL_INFO, "Timer active" )
	else:
		log.Add( log.LEVEL_INFO, "Timer inactive" )
