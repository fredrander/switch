import log
import pytz
import settings
import datetime
import sun


def getLocalDateTime():
	tz = pytz.timezone( settings.TIME_ZONE )
	t = tz.localize( datetime.datetime.now() )
	return t


def getSunriseSunset( localDateTime ):
	s = sun.sun( lat = settings.LATITUDE, long = settings.LONGITUDE )
	sunrise = s.sunrise(localDateTime)
	noon = s.solarnoon(localDateTime)
	sunset = s.sunset(localDateTime)
	result = {}
	result["sunrise"] = sunrise
	result["noon"] = noon
	result["sunset"] = sunset
	return result


def isSunUp( localDateTime, sunriseSunset ):
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


def active():
	dt = getLocalDateTime()
	s = getSunriseSunset(dt)
	sunUp = isSunUp(dt, s)
	if sunUp:
		log.Add( log.LEVEL_INFO, "Sun is up" )
		return False
	else:
		log.Add( log.LEVEL_INFO, "Sun is down" )
		return True

